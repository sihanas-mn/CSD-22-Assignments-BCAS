select Staff_name, Email_ID from Staff where Staff_ID='ST03' --Q3

select Staff_ID, Phone_no from Department, Staff where Dept_Name='Mechatronics' and Staff_ID=HOD_Staff_ID; --Q4

select* from Staff where Phone_no='753758761';--Q4

select Dept_Name, Course_Name from Staff, Department, Course where Staff_Name='SJ. Nisansala' and Staff_ID=HOD_Staff_ID and Dept_no=Offering_Dept_no; --Q5

