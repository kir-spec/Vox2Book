use eframe::egui;
use rfd::FileDialog;
use std::path::PathBuf;
use crate::config::AppConfig;
use crate::models::{Genre, LiteratureElement};
use crate::process_literature_project;
use crate::logger::VoxLogger;

pub struct Vox2BookApp {
    input_path: String,
    output_path: String,
    genre: Genre,
    api_provider: String,
    api_key: String,
    model_name: String,
    title: String,
    subtitle: String,
    status_message: String,
    is_success: bool,
    processed_elements: Vec<LiteratureElement>,
    last_saved_path: Option<PathBuf>,
    show_logs: bool,
    show_preview: bool,
}

impl Default for Vox2BookApp {
    fn default() -> Self {
        let config = AppConfig::load_or_default("config.json");
        Self {
            input_path: String::new(),
            output_path: String::new(),
            genre: Genre::Auto,
            api_provider: config.api_provider,
            api_key: config.api_key,
            model_name: config.model,
            title: config.title,
            subtitle: config.subtitle,
            status_message: "Готово к работе. Выберите файл для вычистки.".to_string(),
            is_success: false,
            processed_elements: Vec::new(),
            last_saved_path: None,
            show_logs: false,
            show_preview: false,
        }
    }
}

impl Vox2BookApp {
    pub fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        Self::default()
    }

    fn select_input_file(&mut self) {
        if let Some(path) = FileDialog::new()
            .add_filter("Литературные файлы", &["txt", "md", "html", "docx"])
            .pick_file()
        {
            self.set_input_path(path);
        }
    }

    fn select_input_folder(&mut self) {
        if let Some(path) = FileDialog::new().pick_folder() {
            self.set_input_path(path);
        }
    }

    fn set_input_path(&mut self, path: PathBuf) {
        self.input_path = path.to_string_lossy().to_string();
        let mut out = path.clone();
        if path.is_file() {
            out.set_extension("docx");
        } else {
            out.push("book_processed.docx");
        }
        self.output_path = out.to_string_lossy().to_string();
        self.status_message = format!("Загружен файл: {}", path.file_name().unwrap_or_default().to_string_lossy());
        self.is_success = false;
        VoxLogger::info("GUI", &format!("Selected input path: {:?}", path));
    }

    fn save_current_config(&self) {
        let cfg = AppConfig {
            api_provider: self.api_provider.clone(),
            api_key: self.api_key.clone(),
            model: self.model_name.clone(),
            ollama_url: "http://localhost:11434".to_string(),
            lmstudio_url: "http://localhost:1234".to_string(),
            genre: self.genre.to_string(),
            title: self.title.clone(),
            subtitle: self.subtitle.clone(),
        };
        if let Ok(json_str) = serde_json::to_string_pretty(&cfg) {
            let _ = std::fs::write("config.json", json_str);
        }
    }
}

impl eframe::App for Vox2BookApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if !ctx.input(|i| i.raw.dropped_files.is_empty()) {
            ctx.input(|i| {
                if let Some(file) = i.raw.dropped_files.first() {
                    if let Some(path) = &file.path {
                        self.set_input_path(path.clone());
                    }
                }
            });
        }

        let mut visuals = egui::Visuals::dark();
        visuals.window_rounding = egui::Rounding::same(12.0);
        visuals.widgets.noninteractive.bg_fill = egui::Color32::from_rgb(15, 20, 28);
        visuals.widgets.inactive.bg_fill = egui::Color32::from_rgb(26, 34, 48);
        visuals.widgets.hovered.bg_fill = egui::Color32::from_rgb(38, 50, 70);
        visuals.widgets.active.bg_fill = egui::Color32::from_rgb(0, 120, 255);
        ctx.set_visuals(visuals);

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.add_space(6.0);

            // Header Banner
            ui.horizontal(|ui| {
                ui.add_space(4.0);
                ui.label(egui::RichText::new("📚").size(28.0));
                ui.vertical(|ui| {
                    ui.horizontal(|ui| {
                        ui.heading(
                            egui::RichText::new("Vox2Book")
                                .size(22.0)
                                .strong()
                                .color(egui::Color32::from_rgb(0, 153, 255)),
                        );
                        ui.label(
                            egui::RichText::new("v2.4.0 (LM Studio & Ollama AI)")
                                .size(11.0)
                                .strong()
                                .color(egui::Color32::from_rgb(229, 169, 60)),
                        );
                    });
                    ui.label(
                        egui::RichText::new("Шлюз нейросетей (LM Studio, Ollama, OpenAI, DeepSeek, Claude) и верстальщик книг")
                            .size(12.0)
                            .color(egui::Color32::from_rgb(156, 163, 175)),
                    );
                });
            });

            ui.add_space(6.0);
            ui.separator();
            ui.add_space(6.0);

            // 1. Neural API Connection Settings Card
            ui.group(|ui| {
                ui.label(egui::RichText::new("🔑 Подключение к Нейросети и API Ключи:").size(13.0).strong().color(egui::Color32::from_rgb(0, 153, 255)));
                ui.add_space(4.0);

                ui.horizontal_wrapped(|ui| {
                    ui.label("Провайдер:");
                    if ui.selectable_label(self.api_provider == "lmstudio", "🖥️ LM Studio (Локально)").clicked() {
                        self.api_provider = "lmstudio".to_string();
                        self.model_name = "local-model".to_string();
                        self.save_current_config();
                    }
                    if ui.selectable_label(self.api_provider == "ollama", "🤖 Ollama (Локально)").clicked() {
                        self.api_provider = "ollama".to_string();
                        self.model_name = "llama3".to_string();
                        self.save_current_config();
                    }
                    if ui.selectable_label(self.api_provider == "openai", "☁️ OpenAI (GPT-4o)").clicked() {
                        self.api_provider = "openai".to_string();
                        self.model_name = "gpt-4o-mini".to_string();
                        self.save_current_config();
                    }
                    if ui.selectable_label(self.api_provider == "deepseek", "☁️ DeepSeek API").clicked() {
                        self.api_provider = "deepseek".to_string();
                        self.model_name = "deepseek-chat".to_string();
                        self.save_current_config();
                    }
                    if ui.selectable_label(self.api_provider == "anthropic", "☁️ Claude API").clicked() {
                        self.api_provider = "anthropic".to_string();
                        self.model_name = "claude-3-5-sonnet-20240620".to_string();
                        self.save_current_config();
                    }
                });

                ui.add_space(4.0);

                if self.api_provider == "lmstudio" {
                    ui.label(egui::RichText::new("🖥️ Адрес подключения LM Studio: http://localhost:1234/v1 (Локальный сервер)").size(11.5).color(egui::Color32::from_rgb(16, 185, 129)));
                } else if self.api_provider == "ollama" {
                    ui.label(egui::RichText::new("🤖 Адрес подключения Ollama: http://localhost:11434 (Локальный сервер)").size(11.5).color(egui::Color32::from_rgb(16, 185, 129)));
                } else {
                    egui::Grid::new("api_key_grid").num_columns(2).spacing([10.0, 4.0]).show(ui, |ui| {
                        ui.label("API Ключ:");
                        let mut key_edit = self.api_key.clone();
                        if ui.add_sized([ui.available_width(), 24.0], egui::TextEdit::singleline(&mut key_edit).password(true).hint_text("Вставьте API Ключ (sk-...)")).changed() {
                            self.api_key = key_edit;
                            self.save_current_config();
                        }
                        ui.end_row();
                    });
                }
            });

            ui.add_space(6.0);

            // 2. File Input Drop Zone
            egui::Frame::none()
                .fill(egui::Color32::from_rgb(21, 28, 40))
                .rounding(egui::Rounding::same(8.0))
                .stroke(egui::Stroke::new(1.0, egui::Color32::from_rgb(34, 46, 66)))
                .inner_margin(egui::Margin::same(8.0))
                .show(ui, |ui| {
                    ui.horizontal(|ui| {
                        ui.label(egui::RichText::new("📥 Входной файл / расшифровка:").size(13.0).strong());
                        ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                            if ui.add(egui::Button::new("📂 Папка")).clicked() {
                                self.select_input_folder();
                            }
                            if ui.add(egui::Button::new("📄 Файл")).clicked() {
                                self.select_input_file();
                            }
                        });
                    });
                    ui.add_space(4.0);
                    ui.add_sized(
                        [ui.available_width(), 26.0],
                        egui::TextEdit::singleline(&mut self.input_path)
                            .hint_text("Перетащите сюда файл текста (.txt, .md, .docx) или нажмите Выбрать..."),
                    );
                });

            ui.add_space(6.0);

            // 3. Genre Selector Cards
            ui.group(|ui| {
                ui.label(egui::RichText::new("Жанровый режим макетирования:").size(13.0).strong().color(egui::Color32::from_rgb(229, 169, 60)));
                ui.add_space(4.0);

                ui.horizontal_wrapped(|ui| {
                    ui.selectable_value(&mut self.genre, Genre::Auto, "🤖 Авто-анализ");
                    ui.selectable_value(&mut self.genre, Genre::Prose, "📖 Проза / Роман");
                    ui.selectable_value(&mut self.genre, Genre::Poetry, "✍️ Поэзия / Стихи");
                    ui.selectable_value(&mut self.genre, Genre::Drama, "🎭 Драматургия");
                    ui.selectable_value(&mut self.genre, Genre::Dialogue, "💬 Диалоги");
                });
            });

            ui.add_space(6.0);

            // 4. Metadata Settings
            ui.group(|ui| {
                ui.label(egui::RichText::new("Настройки книги и экспорта:").size(13.0).strong().color(egui::Color32::from_rgb(16, 185, 129)));
                ui.add_space(4.0);

                egui::Grid::new("meta_grid").num_columns(2).spacing([12.0, 4.0]).show(ui, |ui| {
                    ui.label("Название книги:");
                    ui.add_sized([ui.available_width(), 24.0], egui::TextEdit::singleline(&mut self.title).hint_text("Необязательно"));
                    ui.end_row();

                    ui.label("Файл сохранения:");
                    ui.horizontal(|ui| {
                        ui.add_sized(
                            [ui.available_width() - 100.0, 24.0],
                            egui::TextEdit::singleline(&mut self.output_path).hint_text("Путь к итоговому .docx"),
                        );
                        if ui.add(egui::Button::new("Сохранить как")).clicked() {
                            if let Some(path) = FileDialog::new()
                                .add_filter("Word Document", &["docx"])
                                .save_file()
                            {
                                self.output_path = path.to_string_lossy().to_string();
                            }
                        }
                    });
                    ui.end_row();
                });
            });

            ui.add_space(10.0);

            // 5. Action Button
            ui.vertical_centered(|ui| {
                let btn = egui::Button::new(
                    egui::RichText::new("🚀 ВЫЧИТАТЬ ЧЕРЕЗ API И СФОРМИРОВАТЬ МАКЕТ DOCX")
                        .size(15.0)
                        .strong()
                        .color(egui::Color32::WHITE),
                )
                .fill(egui::Color32::from_rgb(0, 120, 255))
                .min_size(egui::vec2(400.0, 42.0));

                if ui.add(btn).clicked() {
                    self.save_current_config();

                    if self.input_path.trim().is_empty() {
                        self.status_message = "❌ Ошибка: Пожалуйста, выберите входной файл!".to_string();
                        self.is_success = false;
                    } else {
                        let in_p = PathBuf::from(self.input_path.trim());
                        let out_p = if self.output_path.trim().is_empty() {
                            let mut p = in_p.clone();
                            if p.is_file() {
                                p.set_extension("docx");
                            } else {
                                p.push("book_processed.docx");
                            }
                            p
                        } else {
                            PathBuf::from(self.output_path.trim())
                        };

                        let t_opt = if self.title.trim().is_empty() { None } else { Some(self.title.trim()) };
                        let sub_opt = if self.subtitle.trim().is_empty() { None } else { Some(self.subtitle.trim()) };

                        match process_literature_project(&in_p, &out_p, self.genre.clone(), t_opt, sub_opt) {
                            Ok(elements) => {
                                self.processed_elements = elements.clone();
                                self.last_saved_path = Some(out_p.clone());
                                self.status_message = format!("✅ Успешно обработано через {}! Элементов: {}. Сохранено: {:?}", self.api_provider, elements.len(), out_p);
                                self.is_success = true;
                                self.show_preview = true;
                            }
                            Err(e) => {
                                self.status_message = format!("❌ Ошибка: {}", e);
                                self.is_success = false;
                            }
                        }
                    }
                }
            });

            ui.add_space(6.0);

            // 6. Status Banner
            let banner_color = if self.is_success {
                egui::Color32::from_rgb(16, 185, 129)
            } else if self.status_message.starts_with('❌') {
                egui::Color32::from_rgb(220, 38, 38)
            } else {
                egui::Color32::from_rgb(31, 41, 55)
            };

            egui::Frame::none()
                .fill(banner_color)
                .rounding(egui::Rounding::same(8.0))
                .inner_margin(egui::Margin::same(8.0))
                .show(ui, |ui| {
                    ui.horizontal(|ui| {
                        ui.label(
                            egui::RichText::new(&self.status_message)
                                .size(12.0)
                                .strong()
                                .color(egui::Color32::WHITE),
                        );
                        ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                            if self.is_success {
                                if ui.add(egui::Button::new("📂 Открыть папку")).clicked() {
                                    if let Some(path) = &self.last_saved_path {
                                        if let Some(parent) = path.parent() {
                                            let _ = std::process::Command::new("explorer").arg(parent).spawn();
                                        }
                                    }
                                }
                                let prev_btn_text = if self.show_preview { "🔍 Скрыть сравнение" } else { "🔍 Сравнение До/После" };
                                if ui.add(egui::Button::new(prev_btn_text)).clicked() {
                                    self.show_preview = !self.show_preview;
                                }
                            }
                            let log_btn_text = if self.show_logs { "📋 Скрыть логи" } else { "📋 Показать логи" };
                            if ui.add(egui::Button::new(log_btn_text)).clicked() {
                                self.show_logs = !self.show_logs;
                            }
                        });
                    });
                });

            // 7. Preview Panel
            if self.show_preview && !self.processed_elements.is_empty() {
                ui.add_space(4.0);
                egui::Frame::none()
                    .fill(egui::Color32::from_rgb(18, 24, 34))
                    .rounding(egui::Rounding::same(8.0))
                    .stroke(egui::Stroke::new(1.0, egui::Color32::from_rgb(0, 153, 255)))
                    .inner_margin(egui::Margin::same(8.0))
                    .show(ui, |ui| {
                        ui.label(egui::RichText::new("🔍 Результаты обработки через API (До → После):").size(12.0).strong().color(egui::Color32::from_rgb(0, 153, 255)));
                        ui.add_space(2.0);

                        egui::ScrollArea::vertical()
                            .max_height(100.0)
                            .auto_shrink([false, false])
                            .show(ui, |ui| {
                                for (idx, elem) in self.processed_elements.iter().enumerate().take(8) {
                                    if !elem.body.is_empty() {
                                        ui.horizontal(|ui| {
                                            ui.label(egui::RichText::new(format!("#{}:", idx + 1)).size(11.0).strong().color(egui::Color32::from_rgb(229, 169, 60)));
                                            ui.vertical(|ui| {
                                                ui.label(egui::RichText::new(format!("Было:  {}", elem.body)).size(11.0).color(egui::Color32::from_rgb(239, 68, 68)));
                                                ui.label(egui::RichText::new(format!("Стало: {}", elem.edited_body)).size(11.0).color(egui::Color32::from_rgb(16, 185, 129)));
                                            });
                                        });
                                        ui.separator();
                                    }
                                }
                            });
                    });
            }

            // 8. Logs Panel
            if self.show_logs {
                ui.add_space(4.0);
                egui::Frame::none()
                    .fill(egui::Color32::from_rgb(10, 14, 20))
                    .rounding(egui::Rounding::same(6.0))
                    .stroke(egui::Stroke::new(1.0, egui::Color32::from_rgb(34, 46, 66)))
                    .inner_margin(egui::Margin::same(6.0))
                    .show(ui, |ui| {
                        ui.label(egui::RichText::new("📋 Журнал событий (vox2book.log):").size(11.0).strong().color(egui::Color32::from_rgb(0, 153, 255)));
                        ui.add_space(2.0);

                        egui::ScrollArea::vertical()
                            .max_height(90.0)
                            .auto_shrink([false, false])
                            .show(ui, |ui| {
                                for entry in VoxLogger::get_logs() {
                                    let color = if entry.contains("[ERROR]") {
                                        egui::Color32::from_rgb(239, 68, 68)
                                    } else if entry.contains("[WARN]") {
                                        egui::Color32::from_rgb(245, 158, 11)
                                    } else {
                                        egui::Color32::from_rgb(209, 213, 219)
                                    };
                                    ui.label(egui::RichText::new(entry).size(10.5).monospace().color(color));
                                }
                            });
                    });
            }
        });
    }
}

pub fn run_gui() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("Vox2Book — API Gateway & Literature Publishing Engine")
            .with_inner_size([740.0, 640.0])
            .with_min_inner_size([650.0, 540.0]),
        ..Default::default()
    };

    eframe::run_native(
        "Vox2Book — API Gateway & Literature Publishing Engine",
        options,
        Box::new(|cc| Box::new(Vox2BookApp::new(cc))),
    )
}
