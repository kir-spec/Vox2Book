use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Genre {
    Auto,
    Prose,
    Poetry,
    Drama,
    Dialogue,
    Academic,
}

impl fmt::Display for Genre {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Genre::Auto => write!(f, "Auto-detect"),
            Genre::Prose => write!(f, "Prose / Novel"),
            Genre::Poetry => write!(f, "Poetry / Verse"),
            Genre::Drama => write!(f, "Drama / Play"),
            Genre::Dialogue => write!(f, "Dialogue / Oral Chronicle"),
            Genre::Academic => write!(f, "Academic / Article"),
        }
    }
}

impl Genre {
    pub fn from_str(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            "prose" => Genre::Prose,
            "poetry" => Genre::Poetry,
            "drama" => Genre::Drama,
            "dialogue" => Genre::Dialogue,
            "academic" => Genre::Academic,
            _ => Genre::Auto,
        }
    }
}

#[derive(Debug, Clone)]
pub enum ElementType {
    Heading,
    Paragraph,
    VerseLine,
    StanzaBreak,
    CharacterName,
    StageDirection,
    Message {
        msg_type: String, // "voice" or "text"
        time_str: String,
        timestamp: String,
    },
}

#[derive(Debug, Clone)]
pub struct LiteratureElement {
    pub element_type: ElementType,
    pub body: String,
    pub edited_body: String,
    pub speaker: Option<String>,
}
