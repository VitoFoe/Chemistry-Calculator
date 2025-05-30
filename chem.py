import ttkbootstrap as ttkb
from PIL import Image, ImageTk
import tkinter
from tkinter import messagebox
import math
import os

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chemistry Formula Calculator")
        self.root.geometry("850x500")
        self.chosenData = {}

        ttkb.Label(root, text="Choose a Formula:").pack(pady=5)
        self.combo_chemform = ttkb.Combobox(root, values=["Moles With Ar or Mr", "Moles With Coefficients", "Molarity With Volume", "Volume At STP", "Percent Composition"], bootstyle="secondary")
        self.combo_chemform.pack()
        self.combo_chemform.bind("<<ComboboxSelected>>", self.showForm)

        self.main_frame = ttkb.Frame(root)
        self.main_frame.pack(pady=10)

        self.input_frame = ttkb.Frame(self.main_frame)
        self.input_frame.grid(row=0, column=0, padx=10)

        self.image_frame = ttkb.Frame(self.main_frame)
        self.image_frame.grid(row=0, column=1, padx=10)

        ttkb.Button(root, text="Calculate", command=self.calculate, bootstyle="secondary").pack(pady=5)

        self.result = ttkb.StringVar()
        ttkb.Label(root, textvariable=self.result, bootstyle="dark").pack(pady=5)

    def showForm(self, event):
        self.chosenData.clear()
        chemForm = self.combo_chemform.get()

        for widget in self.input_frame.winfo_children():
            widget.destroy()

        for widget in self.image_frame.winfo_children():
            widget.destroy()

        self.displayImage(chemForm)

        if chemForm == "Moles With Ar or Mr":
            for i, label in enumerate(["Gr", "Ar or Mr"]):
                ttkb.Label(self.input_frame, text=label + " :").grid(row=i, column=0)
                self.chosenData[label.lower()] = ttkb.Entry(self.input_frame, bootstyle="secondary")
                self.chosenData[label.lower()].grid(row=i, column=1)

        elif chemForm == "Moles With Coefficients":
            for i, label in enumerate(["Coef. Asked", "Coef. Given", "Mol Given"]):
                ttkb.Label(self.input_frame, text=label + " :").grid(row=i, column=0)
                self.chosenData[label.lower()] = ttkb.Entry(self.input_frame, bootstyle="secondary")
                self.chosenData[label.lower()].grid(row=i, column=1)
                
        elif chemForm == "Molarity With Volume":
            for i, label in enumerate(["Mol", "V"]):
                ttkb.Label(self.input_frame, text=label + " :").grid(row=i, column=0)
                self.chosenData[label.lower()] = ttkb.Entry(self.input_frame, bootstyle="secondary")
                self.chosenData[label.lower()].grid(row=i, column=1)

        elif chemForm == "Volume At STP":
            ttkb.Label(self.input_frame, text="Mol :").grid(row=0, column=0)
            self.chosenData['mol'] = ttkb.Entry(self.input_frame, bootstyle="secondary")
            self.chosenData['mol'].grid(row=0, column=1)

        elif chemForm == "Percent Composition":
            for i, label in enumerate(["i", "Ar", "Mr"]):
                ttkb.Label(self.input_frame, text=label + " :").grid(row=i, column=0)
                self.chosenData[label.lower()] = ttkb.Entry(self.input_frame, bootstyle="secondary")
                self.chosenData[label.lower()].grid(row=i, column=1)

    def displayImage(self, chemform):
        path = f"formulas/{chemform.lower()}.png"
        if os.path.exists(path):
            img = Image.open(path)
            img = img.resize((450, 250))
            photo = ImageTk.PhotoImage(img)
            label_img = ttkb.Label(self.image_frame, image=photo)
            label_img.image = photo
            label_img.pack()
        else:
            ttkb.Label(self.image_frame, text="Image Not Found.").pack()

    def calculate(self):
        chemForm = self.combo_chemform.get()
        
        try:
            if chemForm == "Moles With Ar or Mr":
                try:
                    Gr = float(self.chosenData['gr'].get())
                    ArMr = float(self.chosenData['ar or mr'].get())

                    Mol = Gr / ArMr

                    self.result.set(f"The moles of the molecule / element is {Mol:.3f}")

                except ZeroDivisionError:
                    tkinter.messagebox.showerror("Error", "Ar or Mr cant be zero!")

            elif chemForm == "Moles With Coefficients":
                try:
                    CAsk = float(self.chosenData['coef. asked'].get())
                    CGive = float(self.chosenData['coef. given'].get())
                    MolGive = float(self.chosenData['mol given'].get())
                    
                    MolAsk = (CAsk / CGive) * MolGive

                    self.result.set(f"The moles of the molecule / element asked is {MolAsk:.3f}")

                except ZeroDivisionError:
                    tkinter.messagebox.showerror("Error", "Given Coefficient cant be 0!")

            elif chemForm == "Molarity With Volume":
                try:
                    Mol = float(self.chosenData['mol'].get())
                    V = float(self.chosenData['v'].get())
                    
                    M = Mol / V

                    self.result.set(f"The molarity of the solution is {M:.3f}")

                except ZeroDivisionError:
                    tkinter.messagebox.showerror("Error", "Volume cant be zero!")

            elif chemForm == "Volume At STP":
                Mol = float(self.chosenData['mol'].get())

                V = Mol * 22.4

                self.result.set(f"The volume of the gas at STP is {V:.3f}")
            
            elif chemForm == "Percent Composition":
                try:
                    i = float(self.chosenData['i'].get())
                    Ar = float(self.chosenData['ar'].get())
                    Mr = float(self.chosenData['mr'].get())

                    M = (i * Ar) / Mr * 100

                    self.result.set(f"The molarity of the solution is {M:.3f}%")
                
                except ZeroDivisionError:
                    tkinter.messagebox.showerror("Error", "Mr cant be zero!")
                    
            else:
                self.result.set("Please choose a valid formula.")
                return

        except Exception:
            tkinter.messagebox.showwarning("Error", "Invalid Input!")

if __name__ == "__main__":
    app = ttkb.Window(themename="lumen")
    MainApp(app)
    app.mainloop()