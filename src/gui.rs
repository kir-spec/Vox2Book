use eframe::egui;
use rfd::FileDialog;
use std::path::PathBuf;
use crate::models::Genre;
use crate::process_literature_project;

pub struct Vox2BookApp {
    input_path: String,
    output_path: String,
    genre: Genre,
    title: String,
    subtitle: String,
    status_message: String,
    is_success: bool,
}

impl Default for Vox2BookApp {
    fn default() -> Self {
        Self {
            input_path: String::new(),
            output_path: String::new(),
            genre: Genre::Auto,
            title: String::new(),
            subtitle: String::new(),
            status_message: "Готово к работе. Выберите или перетащите файл.".to_string(),
            is_success: false,
        }
    }
}

impl Vox2BookApp {
    pub fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        Self::default()
    }
}

impl eframe::App for Vox2BookApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Handle Drag & Drop of files onto the window
        if !ctx.input(|i| i.raw.dropped_files.is_empty()) {
            ctx.input(|i| {
                if let Some(file) = i.raw.dropped_files.first() {
                    if let Some(path) = &file.path {
                        self.input_path = path.to_string_lossy().to_string();
                        let mut out = path.clone();
                        out.set_extension("docx");
                        self.output_path = out.to_string_lossy().to_string();
                        self.status_message = format!("Загружен файл: {}", path.file_name().unwrap_or_default().to_string_lossy());
                        self.is_success = false;
                    }
                }
            });
        }

        // Custom Visual Theme & Styling
        let mut visuals = egui::Visuals::dark();
        visuals.window_rounding = egui::Rounding::same(10.0);
        visuals.widgets.noninteractive.bg_fill = egui::Color32::from_rgb(24, 28, 36);
        ctx.set_visuals(visuals);

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.vertical_centered(|ui| {
                ui.add_space(10.0);
                ui.heading(
                    egui::RichText::new("📚 Vox2Book Publishing Engine")
                        .size(24.0)
                        .strong()
                        .color(egui::Color32::from_rgb(90, 160, 245)),
                );
                ui.label(
                    egui::RichText::new("Универсальный издательский комплекс для вычистки и генерации книг в DOCX")
                        .size(13.0)
                        .color(egui::Color32::from_rgb(160, 175, 195)),
                );
                ui.add_space(12.0);
            });

            ui.separator();
            ui.add_space(10.0);

            // 1. File Input Drop Zone & Selector
            ui.group(|ui| {
                ui.heading(egui::RichText::new("1. Входные данные").size(15.0).strong());
                ui.add_space(4.0);

                ui.horizontal(|ui| {
                    ui.add_sized(
                        [ui.available_width() - 110.0, 28.0],
                        egui::TextEdit::singleline(&mut self.input_path)
                            .hint_text("Перетащите файл сюда или нажмите Обзор..."),
                    );

                    if ui.add_sized([100.0, 28.0], egui::Button::new("📁 Обзор...")).clicked() {
                        if let Some(path) = FileDialog::new()
                            .add_filter("Текстовые файлы и документы", &["txt", "md", "html", "docx"])
                            .pick_file()
                        {
                            self.input_path = path.to_string_lossy().to_string();
                            let mut out = path.clone();
                            out.set_extension("docx");
                            self.output_path = out.to_string_lossy().to_string();
                            self.status_message = format!("Загружен файл: {}", path.file_name().unwrap_or_default().to_string_lossy());
                        }
                    }
                });
            });

            ui.add_space(10.0);

            // 2. Genre Selector
            ui.group(|ui| {
                ui.heading(egui::RichText::new("2. Жанр произведения").size(15.0).strong());
                ui.add_space(6.0);

                ui.horizontal_wrapped(|ui| {
                    ui.selectable_value(&mut self.genre, Genre::Auto, "🤖 Автоопределение");
                    ui.selectable_value(&mut self.genre, Genre::Prose, "📖 Проза / Роман");
                    ui.selectable_value(&mut self.genre, Genre::Poetry, "✍️ Поэзия / Стихи");
                    ui.selectable_value(&mut self.genre, Genre::Drama, "🎭 Драматургия / Пьеса");
                    ui.selectable_value(&mut self.genre, Genre::Dialogue, "💬 Устные диалоги");
                });
            });

            ui.add_space(10.0);

            // 3. Metadata Parameters
            ui.group(|ui| {
                ui.heading(egui::RichText::new("3. Оформление и выгрузка").size(15.0).strong());
                ui.add_space(6.0);

                egui::Grid::new("meta_grid").num_columns(2).spacing([12.0, 8.0]).show(ui, |ui| {
                    ui.label("Название книги:");
                    ui.add_sized([ui.available_width(), 26.0], egui::TextEdit::singleline(&mut self.title).hint_text("Необязательно"));
                    ui.end_row();

                    ui.label("Подзаголовок:");
                    ui.add_sized([ui.available_width(), 26.0], egui::TextEdit::singleline(&mut self.subtitle).hint_text("Необязательно"));
                    ui.end_row();

                    ui.label("Файл сохранения:");
                    ui.horizontal(|ui| {
                        ui.add_sized(
                            [ui.available_width() - 110.0, 26.0],
                            egui::TextEdit::singleline(&mut self.output_path).hint_text("Путь к итоговому .docx"),
                        );
                        if ui.add_sized([100.0, 26.0], egui::Button::new("Сохранить как")).clicked() {
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

            ui.add_space(14.0);

            // 4. Big Action Button
            ui.vertical_centered(|ui| {
                let btn = egui::Button::new(
                    egui::RichText::new("🚀 Сформировать печатный макет DOCX")
                        .size(16.0)
                        .strong()
                        .color(egui::Color32::WHITE),
                )
                .fill(egui::Color32::from_rgb(35, 120, 220))
                .min_size(egui::vec2(340.0, 42.0));

                if ui.add(btn).clicked() {
                    if self.input_path.trim().is_empty() {
                        self.status_message = "❌ Ошибка: Пожалуйста, выберите входной файл!".to_string();
                        self.is_success = false;
                    } else {
                        let in_p = PathBuf::from(self.input_path.trim());
                        let out_p = if self.output_path.trim().is_empty() {
                            let mut p = in_p.clone();
                            p.set_extension("docx");
                            p
                        } else {
                            PathBuf::from(self.output_path.trim())
                        };

                        let t_opt = if self.title.trim().is_empty() { None } else { Some(self.title.trim()) };
                        let sub_opt = if self.subtitle.trim().is_empty() { None } else { Some(self.subtitle.trim()) };

                        match process_literature_project(&in_p, &out_p, self.genre.clone(), t_opt, sub_opt) {
                            Ok(elements) => {
                                self.status_message = format!("✅ Успешно! Обработано {} элементов. Файл сохранён: {:?}", elements.len(), out_p);
                                self.is_success = true;
                            }
                            Err(e) => {
                                self.status_message = format!("❌ Ошибка при обработке: {}", e);
                                self.is_success = false;
                            }
                        }
                    }
                }
            });

            ui.add_space(12.0);

            // 5. Status Banner
            let banner_color = if self.is_success {
                egui::Color32::from_rgb(30, 75, 45)
            } else if self.status_message.starts_with('❌') {
                egui::Color32::from_rgb(90, 30, 30)
            } else {
                egui::Color32::from_rgb(32, 38, 48)
            };

            egui::Frame::none()
                .fill(banner_color)
                .rounding(egui::Rounding::same(6.0))
                .inner_margin(egui::Margin::same(10.0))
                .show(ui, |ui| {
                    ui.horizontal(|ui| {
                        ui.label(
                            egui::RichText::new(&self.status_message)
                                .size(13.0)
                                .color(egui::Color32::WHITE),
                        );
                    });
                });
        });
    }
}

pub fn run_gui() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_title("Vox2Book — Publishing Engine GUI")
            .with_inner_size([650.0, 520.0])
            .with_min_inner_size([550.0, 450.0]),
        ..Default::default()
    };

    eframe::run_native(
        "Vox2Book — Publishing Engine GUI",
        options,
        Box::new(|cc| Box::new(Vox2BookApp::new(cc))),
    )
}
