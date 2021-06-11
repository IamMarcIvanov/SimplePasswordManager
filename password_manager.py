import string
import random
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box
from rich.prompt import Prompt
from rich.prompt import IntPrompt
from typing import Union
import datetime


console = Console()

class PasswordManager:
    def __init__(self, key_path: str = r'D:\LibraryOfBabel\Projects\PasswordManager\Key.csv'):
        self.key_path = key_path
        try:
            try:
                self.database = pd.read_csv(self.key_path, index_col='No', sep=' ')
            except FileNotFoundError:
                console.print('[bright_red]File was not found. Creating new passwords file[/bright_red]')
                with open(self.key_path, 'w') as f:
                    f.write('')
                self.database = pd.read_csv(self.key_path)
        except pd.errors.EmptyDataError:
            self.database = pd.DataFrame({'No': [], 'NAME': [], 'USERNAME': [], 'EMAIL': [], 'PASSWORD': [], 'NOTES': []})
            self.database.set_index('No', inplace=True)
            self.database.to_csv(self.key_path, line_terminator='\n', sep=' ')
        self.start_interface()
        self.database.to_csv(self.key_path, line_terminator='\n', sep=' ')
    
    def print_entries(self, db: Union[pd.DataFrame, pd.Series], name: str = '', pos: int = 0):
        table = Table(title='[bright_green]{}[/bright_green]'.format(name), box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column('No', style='bright_yellow')
        table.add_column('Name', style='bright_green')
        table.add_column('Username', style='bright_cyan')
        table.add_column('Email', style='bright_red')
        table.add_column('Password', style='bright_magenta')
        table.add_column('Notes', style='bright_blue')
        try:
            for i, row in db.iterrows():
                table.add_row(str(i), str(row['NAME']), str(row['USERNAME']), str(row['EMAIL']), str(row['PASSWORD']), str(row['NOTES']))
            console.print(table)
            console.print('\n\n')
        except AttributeError:
            table.add_row(str(pos), str(db['NAME']), str(db['USERNAME']), str(db['EMAIL']), str(db['PASSWORD']), str(db['NOTES']))
            console.print(table)
            console.print('\n\n')
            
    def search(self, name: str) -> pd.DataFrame:
        return self.database.loc[self.database.NAME.str.lower().str.find(name.lower()) != -1]
    
    def action_table(self, keyword: str):
        table = Table(title='Action: {}'.format(keyword), box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column('Key', style='bright_yellow')
        table.add_column('Meaning', style='bright_green')
        table.add_row('1', 'Name')
        table.add_row('2', 'Username')
        table.add_row('3', 'Email')
        table.add_row('4', 'Password')
        table.add_row('5', 'Notes')
        table.add_row('6', 'Done / Exit')
        console.print(table)
        console.print('\n\n')
        
    def search_logic(self):
        console.print('You have chosen to search')
        name = Prompt.ask('Enter string to search for')
        matches = self.search(name)
        if len(matches) == 0:
            console.print('[bright_red]No entries with given name[/bright_red]')
            console.print('\n\n')
            return
        self.print_entries(matches, name)
        nos = IntPrompt.ask('Enter No of entry to choose it', choices=list(map(str, matches.index.values)))

        while True:
            self.print_entries(self.database.iloc[nos-1], pos=nos)
            self.action_table(keyword='copy to clipboard')
            chosen = Prompt.ask('Copy to clipboard or exit', choices=list(map(str, range(1, 7))))
            if chosen == '1':
                df = pd.DataFrame([self.database.iloc[nos-1]['NAME']])
                df.to_clipboard(index=False, header=False)
                console.print('[bright_red]Added name to clipboard[/bright_red]')
                console.print('\n\n')
            elif chosen == '2':
                df = pd.DataFrame([self.database.iloc[nos-1]['USERNAME']])
                df.to_clipboard(index=False, header=False)
                console.print('[bright_red]Added username to clipboard[/bright_red]')
                console.print('\n\n')
            elif chosen == '3':
                df = pd.DataFrame([self.database.iloc[nos-1]['EMAIL']])
                df.to_clipboard(index=False, header=False)
                console.print('[bright_red]Added email to clipboard[/bright_red]')
                console.print('\n\n')
            elif chosen == '4':
                df = pd.DataFrame([self.database.iloc[nos-1]['PASSWORD']])
                df.to_clipboard(index=False, header=False)
                console.print('[bright_red]Added password to clipboard[/bright_red]')
                console.print('\n\n')
            elif chosen == '5':
                df = pd.DataFrame([self.database.iloc[nos-1]['NOTES']])
                df.to_clipboard(index=False, header=False)
                console.print('[bright_red]Added notes to clipboard[/bright_red]')
                console.print('\n\n')
            else:
                console.print('[bright_yellow]We assume your work is done[/bright_yellow]')
                console.print('\n\n')
                break
                
    def make_home_table(self):
        self.home = Table(title='PASSWORD MANAGER', box=box.MINIMAL_DOUBLE_HEAD)
        self.home.add_column('Key', style='bright_yellow')
        self.home.add_column('Meaning', style='bright_green')
        self.home.add_row('1', 'Search')
        self.home.add_row('2', 'Insert')
        self.home.add_row('3', 'Delete')
        self.home.add_row('4', 'Update')
        self.home.add_row('5', 'Exit')
    
    def get_email(self) -> str:
        mails = {
            1: 'lordheisenbergpoirot@gmail.com', 
            2: 'f20180103@hyderabad.bits-pilani.ac.in',
            3: 'marcivanovofearth@gmail.com',
            4: 'danish@hertzai.com',
            5: 'danmoham1@publicisgroupe.net',
            6: 'danish.mohammad@epsilon.com',
            7: 'drfarzana31@gmail.com',
        }
        table = Table(title='Email', box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column('Key', style='bright_yellow')
        table.add_column('Meaning', style='bright_green')
        for mail_index in mails.keys():
            table.add_row(str(mail_index), mails[mail_index])
        table.add_row('8', 'Manually Enter Email')
        
        console.print(table)
        console.print('\n\n')
        mail_choice = IntPrompt.ask('Choose mail', choices=list(map(str, range(1, 9))))
        if mail_choice in list(range(1, 8)):
            return mails[mail_choice]
        else:
            return Prompt.ask('Enter email')
    
    def generate_password(self, length: int, n_lowercase: int, n_uppercase: int, n_special_characters: int, n_numbers: int):
        n_unspecified = length - (n_lowercase + n_uppercase + n_special_characters + n_numbers)
        ans = (random.choices(string.ascii_lowercase, k=n_lowercase)
              + random.choices(string.ascii_uppercase, k=n_uppercase)
              + random.choices(string.digits, k=n_numbers)
              + random.choices(string.punctuation, k= n_special_characters)
              + random.choices(string.ascii_letters + string.digits, k = max(0, n_unspecified)))
        random.shuffle(ans)
        return ''.join(ans)
    
    def get_password(self) -> str:
        table = Table(title='Password', box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column('Key', style='bright_yellow')
        table.add_column('Meaning', style='bright_green')
        table.add_row('1', 'Generate Password')
        table.add_row('2', 'Manually Enter Password')
        console.print(table)
        console.print('\n\n')
        
        password_method_choice = IntPrompt.ask('Chose mode of password entry', choices=['1', '2'])
        if password_method_choice == 1:
            pwd_len = IntPrompt.ask('Enter required length of password', choices=list(map(str, range(1, 400))))
            min_small = IntPrompt.ask('Enter the minimum number of lowercase letters required', choices=list(map(str, range(399))))
            min_large = IntPrompt.ask('Enter the minimum number of uppercase letters required', choices=list(map(str, range(399))))
            min_special = IntPrompt.ask('Enter the minimum number of special characters required', choices=list(map(str, range(399))))
            min_num = IntPrompt.ask('Enter the minimum number of numeric characters required', choices=list(map(str, range(399))))
            if min_small + min_large + min_special + min_num > pwd_len:
                console.print('[bright_red]The sum of the minimum requirements exceeds the maximum length[/bright_red]')
                console.print("[bright_red]Thus a password will be set for you. Update it if you don't like it[/bright_red]")
                pwd_len, min_small, min_large, min_special, min_num = 30, 5, 5, 5, 5
            return self.generate_password(pwd_len, min_small, min_large, min_special, min_num)
        else:
            return Prompt.ask('Enter password')
        
    
    def insert_logic(self):
        console.print('You have chosen to insert')
        name = Prompt.ask('Enter name to insert')
        matches = self.search(name)
        if len(matches) > 0:
            console.print('[bright_yellow]It seems the entry already exists:[/bright_yellow]')
            self.print_entries(matches, name)
            console.print('[bright_red]Please update entry or enter unique name[/bright_red]')
            console.print('\n\n')
            return
        else:
            console.print('[bright_green]The name is unique. Continuing ...[/bright_green]')
            username = Prompt.ask('Enter username')
            email = self.get_email()
            password = self.get_password()
            notes = str(datetime.datetime.now()) + ' ' + Prompt.ask('Enter notes (except date and time)')
            self.database.loc[self.database.index.max() + 1] = {'NAME': name, 'USERNAME': username, 'EMAIL': email, 'PASSWORD': password, 'NOTES': notes}
        console.print('The following entry has been made')
        self.print_entries(self.database.loc[self.database.index.max()], pos=self.database.index.max())
    
    def update_logic(self):
        console.print('You have chosen to update')
        name = Prompt.ask('Enter name of entry to update')
        matches = self.search(name)
        if len(matches) == 0:
            console.print('There is no entry matching the name.')
            console.print('\n\n')
            return
        else:
            self.print_entries(matches, name)
            nos = IntPrompt.ask('Enter No of entry to choose it', choices=list(map(str, matches.index.values)))
            
            while True:
                self.print_entries(self.database.iloc[nos-1], pos=nos)
                self.action_table(keyword='Update Entry')
                chosen = IntPrompt.ask('Choose field to update', choices=list(map(str, range(1, 7))))
                if chosen == 1:
                    new_name = Prompt.ask('Enter new name')
                    self.database.at[nos, 'NAME'] = new_name
                    console.print('[bright_green]Entered new name[/bright_green]')
                    
                    df = pd.DataFrame([new_name])
                    df.to_clipboard(index=False, header=False)
                    console.print('[bright_red]Added new name to clipboard[/bright_red]')
                    console.print('\n\n')
                if chosen == 2:
                    new_username = Prompt.ask('Enter new username')
                    self.database.at[nos, 'USERNAME'] = new_username
                    console.print('[bright_green]Entered new username[/bright_green]')
                    
                    df = pd.DataFrame([new_username])
                    df.to_clipboard(index=False, header=False)
                    console.print('[bright_red]Added new username to clipboard[/bright_red]')
                    console.print('\n\n')
                if chosen == 3:
                    new_email = self.get_email()
                    self.database.at[nos, 'EMAIL'] = new_email
                    console.print('[bright_green]Entered new email[/bright_green]')
                    
                    df = pd.DataFrame([new_email])
                    df.to_clipboard(index=False, header=False)
                    console.print('[bright_red]Added new email to clipboard[/bright_red]')
                    console.print('\n\n')
                if chosen == 4:
                    new_password = self.get_password()
                    self.database.at[nos, 'PASSWORD'] = new_password
                    console.print('[bright_green]Entered new password[/bright_green]')
                    
                    df = pd.DataFrame([new_password])
                    df.to_clipboard(index=False, header=False)
                    console.print('[bright_red]Added new password to clipboard[/bright_red]')
                    console.print('\n\n')
                if chosen == 5:
                    new_notes = str(datetime.datetime.now()) + ' ' + Prompt.ask('Enter new notes (except date and time)')
                    self.database.at[nos, 'NOTES'] = new_notes
                    console.print('[bright_green]Entered new notes[/bright_green]')
                    
                    df = pd.DataFrame([new_notes])
                    df.to_clipboard(index=False, header=False)
                    console.print('[bright_red]Added new notes to clipboard[/bright_red]')
                    console.print('\n\n')
                if chosen == 6:
                    console.print('[bright_yellow]We assume your work is done[/bright_yellow]')
                    console.print('\n\n')
                    break
    
    def delete_logic(self):
        console.print('You have chosen to delete')
        name = Prompt.ask('Enter name of entry to delete')
        matches = self.search(name)
        if len(matches) == 0:
            console.print('There is no entry matching the name.')
            console.print('\n\n')
            return
        else:
            self.print_entries(matches, name)
            nos = IntPrompt.ask('Enter No of entry to choose it', choices=list(map(str, matches.index.values)))
            self.print_entries(self.database.iloc[nos-1], pos=nos)
            table = Table(title='Delete Confirmation', box=box.MINIMAL_DOUBLE_HEAD)
            table.add_column('Key', style='bright_yellow')
            table.add_column('Meaning', style='bright_green')
            table.add_row('0', 'Do not delete this entry')
            table.add_row('1', 'I am certain that I want to permanently delete this entry')
            surety = IntPrompt.ask('Confirm deletion?', choices=['0', '1'])
            if surety == 1:
                self.database.drop(nos, inplace=True)
                self.database.reset_index(inplace=True)
                console.print('[bright_green]The entry has been deleted[/bright_green]')
                console.print('\n\n')
    
    def start_interface(self):
        self.make_home_table()
        while True:
            console.print(self.home)
            choice = IntPrompt.ask("Enter your choice", choices=list(map(str, range(1, 6))))
            if choice == 1:
                self.search_logic()
            elif choice == 2:
                self.insert_logic()
            elif choice == 3:
                self.delete_logic()
            elif choice == 4:
                self.update_logic()
            else:
                console.print('[bright_green]Hope you enjoyed it! Bye[/bright_green]')
                break
            


if __name__ == '__main__':
    PasswordManager()