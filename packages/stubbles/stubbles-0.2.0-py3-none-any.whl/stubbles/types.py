from enum import Enum


class Language(Enum):
    PYTHON = "Python"
    JAVA = "Java"
    C = "C"
    CPP = "C++"
    JAVASCRIPT = "JavaScript"
    CSHARP = "C#"
    RUBY = "Ruby"
    SWIFT = "Swift"
    GOLANG = "Go"
    PHP = "PHP"
    TYPESCRIPT = "TypeScript"
    KOTLIN = "Kotlin"
    RUST = "Rust"


comments = {
    Language.PYTHON: "#",
    Language.JAVA: "//",
    Language.C: "//",
    Language.CPP: "//",
    Language.JAVASCRIPT: "//",
    Language.CSHARP: "//",
    Language.RUBY: "#",
    Language.SWIFT: "//",
    Language.GOLANG: "//",
    Language.PHP: "//",
    Language.TYPESCRIPT: "//",
    Language.KOTLIN: "//",
    Language.RUST: "//",
}