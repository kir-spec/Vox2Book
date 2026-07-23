use std::fs::OpenOptions;
use std::io::Write;
use std::sync::{Arc, Mutex};
use chrono::Local;

static LOGGER: std::sync::OnceLock<Arc<Mutex<VoxLogger>>> = std::sync::OnceLock::new();

pub struct VoxLogger {
    pub logs: Vec<String>,
    pub file_path: String,
}

impl VoxLogger {
    pub fn global() -> Arc<Mutex<Self>> {
        LOGGER.get_or_init(|| {
            Arc::new(Mutex::new(VoxLogger {
                logs: Vec::new(),
                file_path: "vox2book.log".to_string(),
            }))
        }).clone()
    }

    pub fn log(level: &str, component: &str, message: &str) {
        let timestamp = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
        let log_entry = format!("[{}] [{}] [{}] {}", timestamp, level, component, message);

        println!("{}", log_entry);

        if let Ok(logger_arc) = LOGGER.get_or_init(|| {
            Arc::new(Mutex::new(VoxLogger {
                logs: Vec::new(),
                file_path: "vox2book.log".to_string(),
            })).clone()
        }).lock() {
            let mut writer = logger_arc;
            writer.logs.push(log_entry.clone());

            // Write to vox2book.log file
            if let Ok(mut file) = OpenOptions::new()
                .create(true)
                .append(true)
                .open(&writer.file_path)
            {
                let _ = writeln!(file, "{}", log_entry);
            }
        }
    }

    pub fn info(component: &str, message: &str) {
        Self::log("INFO", component, message);
    }

    pub fn warn(component: &str, message: &str) {
        Self::log("WARN", component, message);
    }

    pub fn error(component: &str, message: &str) {
        Self::log("ERROR", component, message);
    }

    pub fn get_logs() -> Vec<String> {
        if let Ok(logger) = Self::global().lock() {
            return logger.logs.clone();
        }
        Vec::new()
    }
}
