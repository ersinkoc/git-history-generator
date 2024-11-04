#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from random import randint, choice
import subprocess
import sys
import logging

class GitHistoryGenerator:
    def __init__(self):
        self.logger = self._setup_logger()
        self.commit_messages = [
            "Fix bug in {module}",
            "Update documentation for {module}",
            "Add new feature to {module}",
            "Refactor {module} code",
            "Optimize {module} performance",
            "Implement {module} functionality",
            "Add tests for {module}",
            "Improve error handling in {module}",
            "Update dependencies for {module}",
            "Fix security issue in {module}"
        ]
        self.modules = [
            "core", "api", "database", "auth", "utils",
            "frontend", "backend", "tests", "docs", "config"
        ]

    def _setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def generate_commit_message(self):
        message_template = choice(self.commit_messages)
        module = choice(self.modules)
        return message_template.format(module=module)

    def run_command(self, commands):
        try:
            subprocess.run(commands, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {' '.join(commands)}")
            self.logger.error(f"Error: {e.stderr}")
            sys.exit(1)

    def contribute(self, date, file_path):
        commit_message = self.generate_commit_message()
        
        # Create or update random files to make commits more realistic
        file_name = f"src/{choice(self.modules)}/file_{date.strftime('%Y%m%d_%H%M')}.txt"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        
        with open(file_name, 'w') as file:
            file.write(f"{commit_message}\n\nDate: {date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Update README with commit information
        with open(file_path, 'a') as file:
            file.write(f"- {commit_message} ({date.strftime('%Y-%m-%d %H:%M')})\n\n")
        
        self.run_command(['git', 'add', '.'])
        self.run_command([
            'git', 'commit',
            '-m', f"{commit_message}",
            '--date', date.strftime('%Y-%m-%d %H:%M:%S')
        ])

    def main(self, args=None):
        if args is None:
            args = sys.argv[1:]
        
        parser = self._create_argument_parser()
        args = parser.parse_args(args)
        
        # Validate days before (15 years maximum)
        max_days = 15 * 365  # 15 years
        if args.days_before > max_days:
            args.days_before = max_days
            self.logger.warning(f"Days before adjusted to maximum allowed: {max_days} days (15 years)")
        
        if args.days_before < 0:
            sys.exit('days_before must not be negative')
        if args.days_after < 0:
            sys.exit('days_after must not be negative')

        # Create and initialize repository
        curr_date = datetime.now()
        directory = self._setup_repository(args, curr_date)
        
        # Generate commits
        self._generate_commits(args, curr_date, directory)
        
        # Push to remote if specified
        if args.repository:
            self._push_to_remote(args.repository)

        self.logger.info('\nRepository generation completed successfully! 🎉')

    def _create_argument_parser(self):
        parser = argparse.ArgumentParser(description='Generate Git commit history')
        parser.add_argument('-nw', '--no_weekends', action='store_true', default=False,
                          help='do not commit on weekends')
        parser.add_argument('-mc', '--max_commits', type=int, default=10,
                          help='maximum commits per day (1-20, default: 10)')
        parser.add_argument('-fr', '--frequency', type=int, default=80,
                          help='commit frequency percentage (default: 80)')
        parser.add_argument('-r', '--repository', type=str,
                          help='remote git repository URL')
        parser.add_argument('-un', '--user_name', type=str,
                          help='git user.name config override')
        parser.add_argument('-ue', '--user_email', type=str,
                          help='git user.email config override')
        parser.add_argument('-db', '--days_before', type=int, default=365,
                          help='days before current date (max: 5475 [15 years])')
        parser.add_argument('-da', '--days_after', type=int, default=0,
                          help='days after current date')
        return parser

    def _setup_repository(self, args, curr_date):
        directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
        if args.repository:
            start = args.repository.rfind('/') + 1
            end = args.repository.rfind('.')
            directory = args.repository[start:end]

        os.makedirs(directory, exist_ok=True)
        os.chdir(directory)
        
        # Initialize git repository
        self.run_command(['git', 'init', '-b', 'main'])
        
        # Configure git user if specified
        if args.user_name:
            self.run_command(['git', 'config', 'user.name', args.user_name])
        if args.user_email:
            self.run_command(['git', 'config', 'user.email', args.user_email])

        # Create initial project structure
        os.makedirs('src', exist_ok=True)
        for module in self.modules:
            os.makedirs(f'src/{module}', exist_ok=True)

        return directory

    def _generate_commits(self, args, curr_date, directory):
        readme_path = os.path.join(os.getcwd(), 'README.md')
        with open(readme_path, 'w') as f:
            f.write(f"# Project History\n\nGenerated commit history for {directory}\n\n")

        start_date = curr_date.replace(hour=20, minute=0) - timedelta(days=args.days_before)
        total_days = args.days_before + args.days_after
        
        self.logger.info(f"Generating commits from {start_date.date()} to {(start_date + timedelta(total_days)).date()}")
        
        for day in (start_date + timedelta(n) for n in range(total_days)):
            if (not args.no_weekends or day.weekday() < 5) and randint(0, 100) < args.frequency:
                commits_today = randint(1, min(args.max_commits, 20))
                for commit_time in (day + timedelta(minutes=m * 15) for m in range(commits_today)):
                    self.contribute(commit_time, readme_path)

    def _push_to_remote(self, repository):
        self.logger.info("Pushing to remote repository...")
        self.run_command(['git', 'remote', 'add', 'origin', repository])
        self.run_command(['git', 'branch', '-M', 'main'])
        self.run_command(['git', 'push', '-u', 'origin', 'main'])

if __name__ == "__main__":
    generator = GitHistoryGenerator()
    generator.main()
