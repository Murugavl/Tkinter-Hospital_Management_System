import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymongo

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.config(bg=self.clr(245, 245, 245))  

        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["hospital_management"]
        self.collection = self.db["patients"]

        title = tk.Label(self.root, bg=self.clr(92, 132, 179), text="Hospital Management System", bd=3, relief="groove", font=("Times New Roman", 50, "bold"))
        title.pack(side="top", fill="x", pady=10)

        inFrame = tk.Frame(self.root, bd=4, relief="groove", bg=self.clr(169, 202, 226))
        inFrame.place(width=self.width / 3, height=self.height - 180, x=30, y=100)

        idLbl = tk.Label(inFrame, text="Enter ID:", bg=self.clr(169, 202, 226), font=("Times New Roman", 15, "bold"))
        idLbl.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.idIn = tk.Entry(inFrame, width=20, bd=2, font=("Times New Roman", 15))
        self.idIn.grid(row=0, column=1, padx=10, pady=15)

        nameLbl = tk.Label(inFrame, text="Enter Name:", bg=self.clr(169, 202, 226), font=("Times New Roman", 15, "bold"))
        nameLbl.grid(row=1, column=0, padx=20, pady=15, sticky="w")
        self.nameIn = tk.Entry(inFrame, width=20, bd=2, font=("Times New Roman", 15))
        self.nameIn.grid(row=1, column=1, padx=10, pady=15)

        bgLbl = tk.Label(inFrame, text="Blood Group:", bg=self.clr(169, 202, 226), font=("Times New Roman", 15, "bold"))
        bgLbl.grid(row=2, column=0, padx=20, pady=15, sticky="w")
        self.bgIn = tk.Entry(inFrame, width=20, bd=2, font=("Times New Roman", 15))
        self.bgIn.grid(row=2, column=1, padx=10, pady=15)

        desLbl = tk.Label(inFrame, text="Disease:", bg=self.clr(169, 202, 226), font=("Times New Roman", 15, "bold"))
        desLbl.grid(row=3, column=0, padx=20, pady=15, sticky="w")
        self.desIn = tk.Entry(inFrame, width=20, bd=2, font=("Times New Roman", 15))
        self.desIn.grid(row=3, column=1, padx=10, pady=15)

        hpLbl = tk.Label(inFrame, text="Health Points:", bg=self.clr(169, 202, 226), font=("Times New Roman", 15, "bold"))
        hpLbl.grid(row=4, column=0, padx=20, pady=15, sticky="w")
        self.hpIn = tk.Entry(inFrame, width=20, bd=2, font=("Times New Roman", 15))
        self.hpIn.grid(row=4, column=1, padx=10, pady=15)

        medLbl = tk.Label(inFrame, text="Medication:", bg=self.clr(169, 202, 226), font=("Times New Roman", 15, "bold"))
        medLbl.grid(row=5, column=0, padx=20, pady=15, sticky="w")
        self.medIn = tk.Entry(inFrame, width=20, bd=2, font=("Times New Roman", 15))
        self.medIn.grid(row=5, column=1, padx=10, pady=15)

        addrLbl = tk.Label(inFrame, text="Address:", bg=self.clr(169, 202, 226), font=("Times New Roman", 15, "bold"))
        addrLbl.grid(row=6, column=0, padx=20, pady=15, sticky="w")
        self.addrIn = tk.Entry(inFrame, width=20, bd=2, font=("Times New Roman", 15))
        self.addrIn.grid(row=6, column=1, padx=10, pady=15)

        okBtn = tk.Button(inFrame, text="Admit", command=self.insertFun, bd=2, relief="raised", bg=self.clr(0, 142, 220), font=("Times New Roman", 20, "bold"), width=20)
        okBtn.grid(padx=30, pady=25, columnspan=2)

        self.detFrame = tk.Frame(self.root, bd=4, relief="groove", bg=self.clr(197, 223, 199))
        self.detFrame.place(width=self.width / 2 + 180, height=self.height - 180, x=self.width / 3 + 60, y=100)

        pIdLbl = tk.Label(self.detFrame, text="Patient Name:", bg=self.clr(197, 223, 199), font=("Times New Roman", 15))
        pIdLbl.grid(row=0, column=0, padx=10, pady=15, sticky="w")
        self.pIdIn = tk.Entry(self.detFrame, bd=1, width=12, font=("Times New Roman", 15))
        self.pIdIn.grid(row=0, column=1, padx=7, pady=15)

        medicBtn = tk.Button(self.detFrame, command=self.medicsFun, text="Medication", width=10, font=("Times New Roman", 15, "bold"), bd=2, relief="raised")
        medicBtn.grid(row=0, column=2, padx=8, pady=15)

        hpBtn = tk.Button(self.detFrame, command=self.hPointFun, text="Health Points", width=10, font=("Times New Roman", 15, "bold"), bd=2, relief="raised")
        hpBtn.grid(row=0, column=3, padx=8, pady=15)

        disBtn = tk.Button(self.detFrame, command=self.disFun, text="Discharge", width=10, font=("Times New Roman", 15, "bold"), bd=2, relief="raised")
        disBtn.grid(row=0, column=4, padx=8, pady=15)

        viewAllBtn = tk.Button(self.detFrame, command=self.viewAllPatients, text="View All Patients", width=15, font=("Times New Roman", 15, "bold"), bd=2, relief="raised", bg=self.clr(0, 142, 220))
        viewAllBtn.grid(row=0, column=5, padx=8, pady=15)

        self.tabFun()

    def tabFun(self):
        self.tabFrame = tk.Frame(self.detFrame, bd=3, relief="ridge", bg="cyan")
        self.tabFrame.place(width=self.width / 2 + 140, height=self.height - 280, x=12, y=80)

        x_scrol = tk.Scrollbar(self.tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(self.tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(self.tabFrame, columns=("id", "name", "bGroup", "disease", "hPoint", "medi", "addr"),
                                xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set)

        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("id", text="Patient ID")
        self.table.heading("name", text="Patient Name")
        self.table.heading("bGroup", text="Blood Group")
        self.table.heading("disease", text="Disease")
        self.table.heading("hPoint", text="Health Points")
        self.table.heading("medi", text="Medication")
        self.table.heading("addr", text="Patient Address")
        self.table["show"] = "headings"

        self.table.column("id", width=100, anchor="center")
        self.table.column("name", width=150, anchor="center")
        self.table.column("bGroup", width=100, anchor="center")
        self.table.column("disease", width=120, anchor="center")
        self.table.column("hPoint", width=100, anchor="center")
        self.table.column("medi", width=150, anchor="center")
        self.table.column("addr", width=200, anchor="center")

        self.table.pack(fill="both", expand=1)

    def clr(self, r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    def insertFun(self):
        patient_id = self.idIn.get()
        if not patient_id:
            tk.messagebox.showerror("Error", "Patient ID is required.")
            return

        existing_patient = self.collection.find_one({"id": patient_id})
        if existing_patient:
            tk.messagebox.showerror("Error", f"Patient ID {patient_id} already exists.")
            return

        patient = {
            "id": patient_id,
            "name": self.nameIn.get(),
            "bGroup": self.bgIn.get(),
            "disease": self.desIn.get(),
            "hPoint": int(self.hpIn.get()) if self.hpIn.get().isdigit() else 0,
            "medication": self.medIn.get(),
            "addr": self.addrIn.get(),
        }

        if all(patient.values()):
            try:
                self.collection.insert_one(patient)
                self.viewAllPatients()
                tk.messagebox.showinfo("Success", f"Patient {patient['name']} has been admitted.")
                self.clearFun()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
        else:
            tk.messagebox.showerror("Error", "Please fill in all the fields!")


    def updateTable(self):
        patients = self.collection.find()
        for patient in patients:
            self.table.insert('', tk.END, values=(
                patient["id"],
                patient["name"].upper(),
                patient["bGroup"].upper(),
                patient["disease"].upper(),
                str(patient["hPoint"]),
                patient["medication"].upper(),
                patient["addr"].upper()
            ))

    def clearFun(self):
        self.idIn.delete(0, tk.END)
        self.nameIn.delete(0, tk.END)
        self.bgIn.delete(0, tk.END)
        self.desIn.delete(0, tk.END)
        self.hpIn.delete(0, tk.END)
        self.medIn.delete(0, tk.END)
        self.addrIn.delete(0, tk.END)

    def viewAllPatients(self):
        self.table.delete(*self.table.get_children())
        patients = self.collection.find()
        for patient in patients:
            self.table.insert('', tk.END, values=(
                patient["id"],
                patient["name"].upper(),
                patient["bGroup"].upper(),
                patient["disease"].upper(),
                str(patient["hPoint"]),
                patient["medication"].upper(),
                patient["addr"].upper()
            ))

    def medicsFun(self):
        name = self.pIdIn.get().strip()
        if name:
            patient = self.collection.find_one({"name": name})
            if patient:
                self.table.delete(*self.table.get_children())
                self.table.insert('', tk.END, values=(
                    patient["id"], patient["name"], patient["bGroup"],
                    patient["disease"], patient["hPoint"], patient["medication"], patient["addr"]
                ))
            else:
                tk.messagebox.showerror("Error", "Patient not found.")
        else:
            tk.messagebox.showerror("Error", "Please enter the patient's name.")


    def hPointFun(self):
        self.pointFrame = tk.Frame(self.root, bg="light gray", bd=3, relief="ridge")
        self.pointFrame.place(width=400, height=150, x=500, y=200)
        
        lbl = tk.Label(self.pointFrame, text="Enter Point:", bg="light gray", font=("Times New Roman", 15, "bold"))
        lbl.grid(row=0, column=0, padx=20, pady=20)
        
        self.pointIn = tk.Entry(self.pointFrame, width=17, bd=2, font=("Times New Roman", 15, "bold"))
        self.pointIn.grid(row=0, column=1, padx=10, pady=20)
        
        
        okBtn = tk.Button(self.pointFrame, command=self.addPoint, text="Add Point", bd=2, relief="raised", font=("Times New Roman", 15, "bold"), width=15,bg=self.clr(157, 112, 207))
        okBtn.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    def addPoint(self):
        name = self.pIdIn.get().strip()  # Assuming pIdIn now holds the patient's name input
        hp_input = self.pointIn.get().strip()

        if name:
            patient = self.collection.find_one({"name": name})
            if patient:
                try:
                    new_points = int(hp_input)
                    updated_points = new_points + patient["hPoint"]
                    self.collection.update_one({"name": name}, {"$set": {"hPoint": updated_points}})
                    tk.messagebox.showinfo("Success", f"Updated Health Points for patient {name}.")
                    self.viewAllPatients()
                    self.clearFun()
                    self.pointFrame.destroy()  # Close the frame after updating
                except ValueError:
                    tk.messagebox.showerror("Error", "Please enter a valid number for Health Points.")
            else:
                tk.messagebox.showerror("Error", "Patient not found.")
        else:
            tk.messagebox.showerror("Error", "Please enter the patient's name.")

    def disFun(self):
        name = self.pIdIn.get().strip()
        if name:
            patient = self.collection.find_one({"name": name})
            if patient:
                self.collection.delete_one({"name": name})
                tk.messagebox.showinfo("Success", f"Patient {name} has been discharged.")
                self.viewAllPatients()
            else:
                tk.messagebox.showerror("Error", "Patient not found.")
        else:
            tk.messagebox.showerror("Error", "Please enter the patient's name.")


if __name__ == "__main__":
    root = tk.Tk()
    obj = Hospital(root)
    root.mainloop()
