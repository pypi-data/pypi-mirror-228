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
    HTML = "HTML"
    CSS = "CSS"


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
    Language.CSS: "//"

}

extensions = {
    Language.PYTHON: ['.py'],
    Language.JAVA: ['.java'],
    Language.C: ['.c', '.h'],
    Language.CPP: ['.cpp', '.cc', '.cxx', '.hpp'],
    Language.JAVASCRIPT: ['.js', '.jsx'],
    Language.CSHARP: ['.cs'],
    Language.RUBY: ['.rb'],
    Language.SWIFT: ['.swift'],
    Language.GOLANG: ['.go'],
    Language.PHP: ['.php'],
    Language.TYPESCRIPT: ['.ts', '.tsx'],
    Language.KOTLIN: ['.kt', '.kts'],
    Language.RUST: ['.rs'],
    Language.CSS: ['.css', '.scss', '.sass'],
}
