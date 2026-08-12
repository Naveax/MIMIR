fn main() {
    match mimir_cli::run_from(std::env::args_os()) {
        Ok(output) => println!("{output}"),
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    }
}
