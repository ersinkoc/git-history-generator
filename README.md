# Git History Generator

A powerful Python tool to generate a realistic Git commit history, supporting up to 15 years of historical commits. Perfect for testing, demonstration purposes, or populating development portfolios with sample activity patterns.

## 🚀 Features

- Generate commits up to 15 years in the past
- Realistic commit messages and project structure
- Customizable commit frequency and patterns
- Weekend/weekday commit control
- Configurable maximum daily commits
- Support for remote repository push
- Custom git user configuration
- Realistic project structure with multiple modules
- Detailed logging and error handling

## 📋 Requirements

- Python 3.6+
- Git installed and configured on your system
- Internet connection (if pushing to remote repository)

## 💾 Installation

1. Clone this repository:
```bash
git clone https://github.com/ersinkoc/git-history-generator.git
cd git-history-generator
```

2. Make the script executable (Unix-based systems):
```bash
chmod +x git_history_generator.py
```

## 🛠 Usage

### Basic Usage

```bash
python git_history_generator.py
```

### Advanced Usage Examples

1. Generate 15 years of history:
```bash
python git_history_generator.py --days_before 5475
```

2. Generate history excluding weekends:
```bash
python git_history_generator.py --days_before 5475 --no_weekends
```

3. Push to a remote repository:
```bash
python git_history_generator.py --days_before 5475 --repository https://github.com/ersinkoc/git-history-generator.git
```

4. Custom git user configuration:
```bash
python git_history_generator.py --user_name "Your Name" --user_email "your@email.com"
```

5. Customize commit frequency and maximum daily commits:
```bash
python git_history_generator.py --frequency 60 --max_commits 5
```

### Available Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--days_before` | `-db` | Number of days before current date | 365 |
| `--days_after` | `-da` | Number of days after current date | 0 |
| `--no_weekends` | `-nw` | Skip weekend commits | False |
| `--frequency` | `-fr` | Commit frequency percentage | 80 |
| `--max_commits` | `-mc` | Maximum commits per day (1-20) | 10 |
| `--repository` | `-r` | Remote repository URL | None |
| `--user_name` | `-un` | Git user.name config | None |
| `--user_email` | `-ue` | Git user.email config | None |

## 📁 Project Structure

The generated repository will have the following structure:
```
repository-name/
├── README.md
└── src/
    ├── api/
    ├── auth/
    ├── backend/
    ├── config/
    ├── core/
    ├── database/
    ├── docs/
    ├── frontend/
    ├── tests/
    └── utils/
```

## 🎨 Commit Types

The generator creates various types of commits including:
- Bug fixes
- Documentation updates
- Feature additions
- Code refactoring
- Performance optimizations
- Test additions
- Dependency updates
- Security fixes

## ⚠️ Important Notes

1. This tool is for demonstration purposes only
2. Make sure you have appropriate permissions when pushing to remote repositories
3. Maximum history is limited to 15 years (5475 days)
4. Large histories may take some time to generate
5. Ensure you have sufficient disk space for large histories

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 🚫 Disclaimer

This tool is intended for demonstration and testing purposes only. Please use responsibly and in accordance with the terms of service of any platforms you interact with.
