use std::env;
use std::path::PathBuf;
use clap::Parser;
use dialoguer::Input;
use vox2book::models::Genre;
use vox2book::process_literature_project;

#[derive(Parser, Debug)]
#[command(name = "vox2book")]
#[command(author = "kir-spec <https://github.com/kir-spec>")]
#[command(version = "1.0.0")]
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
            println!("Press ENTER to exit...");
            let mut dummy = String::new();
            std::io::stdin().read_line(&mut dummy)?;
            return Ok(());
        }
    }

    // Mode 2: CLI Arguments
    let cli = Cli::parse();

    if let Some(input_path) = cli.input {
        let genre = Genre::from_str(&cli.genre);
        process_literature_project(&input_path, &cli.output, genre, cli.title.as_deref(), cli.subtitle.as_deref())?;
        return Ok(());
    }

    // Mode 3: Interactive Double-Click / Prompt Mode (No args provided)
    println!("=====================================================");
    println!("      📚 Vox2Book Engine — Interactive Assistant     ");
    println!("=====================================================");

    let input_str: String = Input::new()
        .with_prompt("Drag and drop file/folder here or type path")
        .interact_text()?;

    let clean_path = input_str.trim().trim_matches('"').trim_matches('\'');
    let input_path = PathBuf::from(clean_path);

    if !input_path.exists() {
        eprintln!("Error: Path does not exist: {:?}", input_path);
        return Ok(());
    }

    println!("\nSelect Genre:");
    println!("  [1] Prose / Novel (Default)");
    println!("  [2] Poetry / Verse Collection");
    println!("  [3] Drama / Theatre Play");
    println!("  [4] Dialogue / Oral Chronicle");
    println!("  [5] Auto-detect");

    let choice: String = Input::new()
        .with_prompt("Choice [1-5]")
        .default("5".to_string())
        .interact_text()?;

    let genre = match choice.trim() {
        "1" => Genre::Prose,
        "2" => Genre::Poetry,
        "3" => Genre::Drama,
        "4" => Genre::Dialogue,
        _ => Genre::Auto,
    };

    let mut out_path = input_path.clone();
    out_path.set_extension("docx");

    process_literature_project(&input_path, &out_path, genre, None, None)?;

    println!("\n✅ Successfully created manuscript: {:?}", out_path);
    println!("Press ENTER to exit...");
    let mut dummy = String::new();
    std::io::stdin().read_line(&mut dummy)?;

    Ok(())
}
