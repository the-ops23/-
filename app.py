import customtkinter as ctk
import os
import json
import subprocess
import threading

# Always generate the theme file to ensure it's up-to-date (removes need to delete manually)
theme_file = 'red-black.json'
theme = {
    "CTk": {
        "fg_color": ["#000000", "#000000"]
    },
    "CTkToplevel": {
        "fg_color": ["#000000", "#000000"]
    },
    "CTkFrame": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#1A1A1A", "#1A1A1A"],
        "top_fg_color": ["#1A1A1A", "#1A1A1A"],
        "border_color": ["#FF0000", "#CC0000"]
    },
    "CTkButton": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#FF0000", "#CC0000"],
        "hover_color": ["#CC0000", "#AA0000"],
        "border_color": ["#FF0000", "#CC0000"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    },
    "CTkLabel": {
        "corner_radius": 0,
        "fg_color": "transparent",
        "text_color": ["#FFFFFF", "#FFFFFF"]
    },
    "CTkEntry": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#333333", "#333333"],
        "border_color": ["#FF0000", "#CC0000"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "placeholder_text_color": ["#999999", "#999999"]
    },
    "CTkCheckBox": {
        "corner_radius": 6,
        "border_width": 3,
        "fg_color": ["#FF0000", "#CC0000"],
        "border_color": ["#FF0000", "#CC0000"],
        "hover_color": ["#CC0000", "#AA0000"],
        "checkmark_color": ["#FFFFFF", "#FFFFFF"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    },
    "CTkSwitch": {
        "corner_radius": 1000,
        "border_width": 3,
        "button_length": 0,
        "fg_color": ["#333333", "#333333"],
        "progress_color": ["#FF0000", "#CC0000"],
        "button_color": ["#1A1A1A", "#1A1A1A"],
        "button_hover_color": ["#333333", "#333333"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    },
    "CTkRadioButton": {
        "corner_radius": 1000,
        "border_width_checked": 6,
        "border_width_unchecked": 3,
        "fg_color": ["#FF0000", "#CC0000"],
        "border_color": ["#FF0000", "#CC0000"],
        "hover_color": ["#CC0000", "#AA0000"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    },
    "CTkProgressBar": {
        "corner_radius": 1000,
        "border_width": 0,
        "fg_color": ["#333333", "#333333"],
        "progress_color": ["#FF0000", "#CC0000"],
        "border_color": ["#1A1A1A", "#1A1A1A"]
    },
    "CTkSlider": {
        "corner_radius": 1000,
        "button_corner_radius": 1000,
        "border_width": 6,
        "button_length": 0,
        "fg_color": ["#333333", "#333333"],
        "progress_color": ["#FF0000", "#CC0000"],
        "button_color": ["#FF0000", "#CC0000"],
        "button_hover_color": ["#CC0000", "#AA0000"]
    },
    "CTkOptionMenu": {
        "corner_radius": 6,
        "fg_color": ["#FF0000", "#CC0000"],
        "button_color": ["#CC0000", "#AA0000"],
        "button_hover_color": ["#AA0000", "#880000"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    },
    "CTkComboBox": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#333333", "#333333"],
        "border_color": ["#FF0000", "#CC0000"],
        "button_color": ["#FF0000", "#CC0000"],
        "button_hover_color": ["#CC0000", "#AA0000"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    },
    "CTkScrollbar": {
        "corner_radius": 1000,
        "border_spacing": 4,
        "fg_color": "transparent",
        "button_color": ["#FF0000", "#CC0000"],
        "button_hover_color": ["#CC0000", "#AA0000"]
    },
    "CTkSegmentedButton": {
        "corner_radius": 6,
        "border_width": 2,
        "fg_color": ["#333333", "#333333"],
        "selected_color": ["#FF0000", "#CC0000"],
        "selected_hover_color": ["#CC0000", "#AA0000"],
        "unselected_color": ["#1A1A1A", "#1A1A1A"],
        "unselected_hover_color": ["#333333", "#333333"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    },
    "CTkTextbox": {
        "corner_radius": 6,
        "border_width": 0,
        "fg_color": ["#222222", "#222222"],
        "border_color": ["#FF0000", "#CC0000"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "scrollbar_button_color": ["#FF0000", "#CC0000"],
        "scrollbar_button_hover_color": ["#CC0000", "#AA0000"]
    },
    "CTkScrollableFrame": {
        "label_fg_color": ["#FF0000", "#CC0000"]
    },
    "DropdownMenu": {
        "fg_color": ["#333333", "#333333"],
        "hover_color": ["#444444", "#444444"],
        "text_color": ["#FFFFFF", "#FFFFFF"]
    },
    "CTkFont": {
        "macOS": {
            "family": "SF Display",
            "size": 13,
            "weight": "normal"
        },
        "Windows": {
            "family": "Roboto",
            "size": 13,
            "weight": "normal"
        },
        "Linux": {
            "family": "Roboto",
            "size": 13,
            "weight": "normal"
        }
    },
    "CTkTabview": {
        "fg_color": ["#1A1A1A", "#1A1A1A"],
        "border_color": ["#FF0000", "#CC0000"],
        "segmented_button_fg_color": ["#333333", "#333333"],
        "segmented_button_selected_color": ["#FF0000", "#CC0000"],
        "segmented_button_selected_hover_color": ["#CC0000", "#AA0000"],
        "segmented_button_unselected_color": ["#333333", "#333333"],
        "segmented_button_unselected_hover_color": ["#444444", "#444444"],
        "text_color": ["#FFFFFF", "#FFFFFF"],
        "text_color_disabled": ["#999999", "#999999"]
    }
}
with open(theme_file, 'w') as f:
    json.dump(theme, f)

ctk.set_default_color_theme(theme_file)
ctk.set_appearance_mode('dark')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Minecraft Bot Controller')
        self.geometry('600x400')

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill='both', expand=True)

        main_tab = self.tabview.add('Main')
        settings_tab = self.tabview.add('Settings')
        help_tab = self.tabview.add('Help')

        # Settings Tab
        self.num_bots_var = ctk.StringVar(value='1')
        ctk.CTkLabel(settings_tab, text='Amount of Bots').pack(pady=5)
        self.num_combo = ctk.CTkComboBox(settings_tab, values=['1', '2', '3'], variable=self.num_bots_var, command=self.update_fields)
        self.num_combo.pack(pady=5)

        self.type_var = ctk.StringVar(value='Cracked')
        ctk.CTkLabel(settings_tab, text='Account Type').pack(pady=5)
        self.type_combo = ctk.CTkComboBox(settings_tab, values=['Cracked', 'Microsoft'], variable=self.type_var, command=self.update_fields)
        self.type_combo.pack(pady=5)

        ctk.CTkLabel(settings_tab, text='Server IP').pack(pady=5)
        self.server_ip = ctk.CTkEntry(settings_tab, placeholder_text='localhost')
        self.server_ip.pack(pady=5)

        ctk.CTkLabel(settings_tab, text='Server Port').pack(pady=5)
        self.server_port = ctk.CTkEntry(settings_tab, placeholder_text='25565')
        self.server_port.pack(pady=5)

        self.bot_fields = []
        self.update_fields()

        # Main Tab
        self.status_label = ctk.CTkLabel(main_tab, text='Status: Disconnected')
        self.status_label.pack(pady=5)

        self.log = ctk.CTkTextbox(main_tab, state='disabled')
        self.log.pack(padx=10, pady=10, fill='both', expand=True)

        self.command_entry = ctk.CTkEntry(main_tab, placeholder_text='Enter command (e.g., exec /spawn)')
        self.command_entry.pack(pady=10, fill='x')
        self.command_entry.bind('<Return>', self.send_command)

        self.connect_btn = ctk.CTkButton(main_tab, text='Connect', command=self.connect_bots)
        self.connect_btn.pack(pady=10)

        self.bots = []

        # Help Tab
        help_text = ctk.CTkTextbox(help_tab, state='normal')
        help_text.pack(padx=10, pady=10, fill='both', expand=True)
        help_text.insert('0.0', """
Commands List:
- exec <message>: Sends the message in chat (e.g., exec /spawn).
- follow <player>: Follows the specified player using pathfinding.
- stop: Stops all movement and goals.
- mine <blockname>: Mines the nearest block of the given type (e.g., mine diamond_ore).
- attack <player>: Initiates PvP attack on the player.
- equip: Equips the best available armor and tools.
- eat: Manually triggers eating if health is low (auto-eat runs in background).
Note: Bots auto-eat when health drops and manage basic events like chat logging.
""")
        help_text.configure(state='disabled')

    def update_fields(self, _=None):
        for field in self.bot_fields:
            field.destroy()
        self.bot_fields = []
        num = int(self.num_bots_var.get())
        typ = self.type_var.get()
        for i in range(num):
            frame = ctk.CTkFrame(self.tabview.get('Settings'))
            frame.pack(pady=5)
            self.bot_fields.append(frame)
            ctk.CTkLabel(frame, text=f'Bot {i+1}').pack()
            if typ == 'Cracked':
                entry = ctk.CTkEntry(frame, placeholder_text='Username')
                entry.pack()
                setattr(self, f'username_{i}', entry)
            else:
                email = ctk.CTkEntry(frame, placeholder_text='Email')
                email.pack()
                setattr(self, f'email_{i}', email)
                pw = ctk.CTkEntry(frame, placeholder_text='Password', show='*')
                pw.pack()
                setattr(self, f'password_{i}', pw)

    def connect_bots(self):
        if self.bots:
            for proc in self.bots:
                try:
                    proc.stdin.close()
                    proc.terminate()
                except Exception as e:
                    self.log_insert(f'Error disconnecting bot: {e}\n')
            self.bots = []
            self.connect_btn.configure(text='Connect')
            self.status_label.configure(text='Status: Disconnected')
            self.log_insert('Disconnected all bots.\n')
            return

        host = self.server_ip.get() or 'localhost'
        port = self.server_port.get() or '25565'
        num = int(self.num_bots_var.get())
        auth_type = 'offline' if self.type_var.get() == 'Cracked' else 'mojang'  # Note: For full Microsoft auth, consider 'microsoft' with browser login if needed

        self.status_label.configure(text='Status: Connecting...')
        for i in range(num):
            if auth_type == 'offline':
                username = getattr(self, f'username_{i}').get()
                password = ''
            else:
                username = getattr(self, f'email_{i}').get()
                password = getattr(self, f'password_{i}').get()
            args = [host, port, username, password, auth_type]
            try:
                proc = subprocess.Popen(['node', 'bot.js'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
                self.bots.append(proc)
                threading.Thread(target=self.read_log, args=(proc,), daemon=True).start()
            except Exception as e:
                self.log_insert(f'Error starting bot {i+1}: {e}\n')

        self.connect_btn.configure(text='Disconnect')
        self.status_label.configure(text='Status: Connected')
        self.log_insert(f'Connecting {num} bots...\n')

    def read_log(self, proc):
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            self.log_insert(line)

    def send_command(self, event=None):
        cmd = self.command_entry.get()
        if not cmd:
            return
        self.command_entry.delete(0, 'end')
        for proc in self.bots:
            try:
                proc.stdin.write(cmd + '\n')
                proc.stdin.flush()
            except Exception as e:
                self.log_insert(f'Error sending command: {e}\n')
        self.log_insert(f'Sent: {cmd}\n')

    def log_insert(self, text):
        self.log.configure(state='normal')
        self.log.insert('end', text)
        self.log.see('end')
        self.log.configure(state='disabled')

if __name__ == '__main__':
    app = App()
    app.mainloop()
