use std::fs::File;
use std::path::Path;
use docx_rs::*;

use crate::models::{ElementType, Genre, LiteratureElement};

pub fn build_docx_document<P: AsRef<Path>>(
    elements: &[LiteratureElement],
    output_path: P,
    genre: &Genre,
    title: Option<&str>,
    subtitle: Option<&str>,
) -> Result<(), Box<dyn std::error::Error>> {
    let mut doc = Docx::new();

    // 1. Document Title
    let doc_title = title.unwrap_or_else(|| match genre {
        Genre::Prose => "Художественное произведение",
        Genre::Poetry => "Сборник стихотворений",
        Genre::Drama => "Драматическая пьеса",
        Genre::Dialogue => "Устная хроника",
        Genre::Academic => "Академический труд",
        Genre::Auto => "Литературная книга",
    });

    let p_title = Paragraph::new()
        .align(AlignmentType::Center)
        .add_run(
            Run::new()
                .add_text(doc_title)
                .bold()
                .size(44) // 22pt
                .color("1F497D"),
        );
    doc = doc.add_paragraph(p_title);

    // 2. Subtitle
    if let Some(sub) = subtitle {
        let p_sub = Paragraph::new()
            .align(AlignmentType::Center)
            .add_run(
                Run::new()
                    .add_text(sub)
                    .italic()
                    .size(26) // 13pt
                    .color("595959"),
            );
        doc = doc.add_paragraph(p_sub);
    }

    // 3. Process Elements
    for elem in elements {
        let body = if elem.edited_body.is_empty() {
            &elem.body
        } else {
            &elem.edited_body
        };

        match elem.element_type {
            ElementType::Heading => {
                let p = Paragraph::new()
                    .line_spacing(LineSpacing::new().before(280).after(120))
                    .add_run(
                        Run::new()
                            .add_text(body)
                            .bold()
                            .size(32) // 16pt
                            .color("1F497D"),
                    );
                doc = doc.add_paragraph(p);
            }
            ElementType::StanzaBreak => {
                let p = Paragraph::new().line_spacing(LineSpacing::new().after(200));
                doc = doc.add_paragraph(p);
            }
            ElementType::VerseLine => {
                let p = Paragraph::new()
                    .line_spacing(LineSpacing::new().after(20))
                    .indent(Some(720), None, None, None) // Left indent 36pt (720 dxa)
                    .add_run(
                        Run::new()
                            .add_text(body)
                            .size(23)
                            .fonts(RunFonts::new().ascii("Georgia")),
                    );
                doc = doc.add_paragraph(p);
            }
            ElementType::CharacterName => {
                let p = Paragraph::new()
                    .line_spacing(LineSpacing::new().before(160).after(40))
                    .add_run(
                        Run::new()
                            .add_text(body)
                            .bold()
                            .size(22)
                            .fonts(RunFonts::new().ascii("Arial"))
                            .color("1F497D"),
                    );
                doc = doc.add_paragraph(p);
            }
            ElementType::StageDirection => {
                let p = Paragraph::new()
                    .line_spacing(LineSpacing::new().after(80))
                    .add_run(
                        Run::new()
                            .add_text(body)
                            .italic()
                            .size(21)
                            .fonts(RunFonts::new().ascii("Arial"))
                            .color("595959"),
                    );
                doc = doc.add_paragraph(p);
            }
            _ => {
                if !body.is_empty() {
                    let mut p = Paragraph::new().line_spacing(LineSpacing::new().after(120));
                    if matches!(genre, Genre::Prose) && !body.starts_with('—') {
                        p = p.indent(None, Some(SpecialIndentType::FirstLine(360)), None, None);
                    }
                    let font_name = match genre {
                        Genre::Drama => "Arial",
                        Genre::Poetry => "Georgia",
                        _ => "Times New Roman",
                    };
                    p = p.add_run(
                        Run::new()
                            .add_text(body)
                            .size(24)
                            .fonts(RunFonts::new().ascii(font_name)),
                    );
                    doc = doc.add_paragraph(p);
                }
            }
        }
    }

    if let Some(parent) = output_path.as_ref().parent() {
        if !parent.exists() {
            std::fs::create_dir_all(parent)?;
        }
    }

    let file = File::create(output_path)?;
    doc.build().pack(file)?;
    Ok(())
}
