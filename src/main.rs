use std::env;
use std::path::PathBuf;
use clap::Parser;
use vox2book::gui::run_gui;
use vox2book::models::Genre;
use vox2book::process_literature_project;

#[derive(Parser, Debug)]
#[command(name = "vox2book")]
#[command(author = "kir-spec <https://github.com/kir-spec>")]
#[command(version = "1.1.0")]
#[command(about = "Vox2Book — Universal Literature Processing & Publishing Engine")]
struct Cli {
    #[arg(short, long, help = "Path to input text file or folder (.txt, .md, .docx)")]
    input: Option<PathBuf>,

    #[arg(short, long, default_value = "output/book.docx", help = "Output DOCX file path")]
    output: PathBuf,

    #[arg(short, long, default_value = "auto", help = "Genre mode: prose, poetry, drama, dialogue, academic, auto")]
    genre: String,

    #[arg(short, long, help = "Book title")]
    title: Option<String>,

    #[arg(short, long, help = "Book subtitle")]
    subtitle: Option<String>,

    #[arg(long, help = "Force CLI mode instead of GUI window")]
    cli: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<String> = env::args().collect();

    // Mode 1: Drag-and-Drop (a single positional filepath passed without CLI flags)
    if args.len() == 2 && !args[1].starts_with('-') {
        let dragged_path = PathBuf::from(&args[1]);
        if dragged_path.exists() {
            println!("=====================================================");
            println!("   📚 Vox2Book Publishing Engine (Drag-and-Drop)    ");
            println!("=====================================================");
            println!("Processing dragged file: {:?}", dragged_path);

            let mut out_path = dragged_path.clone();
            out_path.set_extension("docx");

            let genre = Genre::Auto;
            process_literature_project(&dragged_path, &out_path, genre, None, None)?;

            println!("\n✅ Done! Book saved to: {:?}", out_path);
            return Ok(());
        }
    }

    // Mode 2: Explicit CLI Arguments
    if args.len() > 1 && (args.iter().any(|a| a.starts_with('-')) || args.contains(&"--cli".to_string())) {
        let cli = Cli::parse();
        if let Some(input_path) = cli.input {
            let genre = Genre::from_str(&cli.genre);
            process_literature_project(&input_path, &cli.output, genre, cli.title.as_deref(), cli.subtitle.as_deref())?;
            return Ok(());
        }
    }

    // Mode 3: Desktop Graphical User Interface Window (GUI) by default!
    println!("Launching Vox2Book Graphical Window Interface...");
    if let Err(e) = run_gui() {
        eprintln!("GUI Error: {}", e);
    }

    Ok(())
}
