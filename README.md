# Udaciy Full Stack Web Developer Nanodegree Project 4: Tournament Results
==========================================================================
This project consists of a vagrant VM, a PostgreSQL migration file, and a
corresponding python module to enable tracking of players and matches in a
swiss system game tournament.

## Prerequisites
- [Vagrant](http://vagrantup.com/)
- [VirtualBox](https://www.virtualbox.org/)

## Setup
1. Clone the repository at https://github.com/sxhan/udacity-fsnd-project-4:
2. cd into the project directory and then the vagrant directory: `cd udacity-fsnd-project-4/vagrant`
3. Launch the Vagrant VM: `vagrant up`. This must be done inside the vagrant directory, where there is a file called `Vagrantfile`
4. Login to the vm: `vagrant ssh`
5. cd to the project directory: `cd /vagrant`
6. Start PostgreSQL set up database/table:
 - Start the PostgreSQL interactive terminal: `psql`
 - Create a database called 'tournament': `CREATE DATABASE tournament;`
 - Run the script for creating tables and views: `\i tournament/tournament.sql`
 - Exit: `\q`
7. Run a test suite to verify the tournament.py module: `python tournament/tournament_test.py`
