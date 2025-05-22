from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils.timezone import now


# class CustomUser(AbstractUser):
#     USER_TYPES = [
#         (1,'admin'),
#         (2,'compuser')
#         (3,'staff'),
#     ]
#     # USER ={
#     #     (1,'admin'),
#     #     (2,'compuser'),
#     #     (3,'superadmin'),
        
#     # }
#     user_type = models.CharField(choices=USER,max_length=50,default=1)

#     # profile_pic = models.ImageField(upload_to='media/profile_pic')
    # profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class CustomUser(AbstractUser):
    USER_TYPES = [
        (1, 'Admin'),
        (2, 'User'),
        (3, 'Staff'),
    ]

    user_type = models.IntegerField(choices=USER_TYPES, default=2)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="teams")
    role = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Supervisor", "Field Agent"
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"
    


class Category(models.Model):
    catname = models.CharField(max_length=200)
    catdes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.catname

class Subcategory(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcatname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subcatname

class State(models.Model):
    statename = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.statename

class UserReg(models.Model):
    # admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"User not associated - {self.mobilenumber}"

# class Complaints(models.Model):
#     URGENCY_LEVELS = [
#         ("Low", "Low"),
#         ("Medium", "Medium"),
#         ("High", "High"),
#         ("Critical", "Critical"),
#     ]

#     userregid = models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
#     cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
#     subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
#     complaint_number = models.IntegerField(default=0)
#     complainttype = models.CharField(max_length=250)
#     stateid = models.ForeignKey(State, on_delete=models.CASCADE)
#     noc = models.CharField(max_length=250)
#     complaindetails = models.TextField(blank=True)
#     compfile = models.ImageField(upload_to='media/doc_file')
#     complaintdate_at = models.DateTimeField(auto_now_add=True)
#     remark = models.TextField(blank=True)
    
#     urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default="Medium")
#     assigned_days = models.IntegerField(default=0)
#     due_date = models.DateField(null=True, blank=True)
    
#     status = models.CharField(max_length=250, default=0)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         urgency_days = {
#             "Low": 10,
#             "Medium": 7,
#             "High": 5,
#             "Critical": 1
#         }

#         # Assign number of days based on urgency
#         self.assigned_days = urgency_days.get(self.urgency, 0)

#         # Ensure complaintdate_at is set before calculating due date
#         if not self.complaintdate_at:
#             self.complaintdate_at = now()

#         # Calculate due date
#         self.due_date = self.complaintdate_at.date() + timedelta(days=self.assigned_days)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Complaint {self.complaint_number} - {self.urgency} - Due {self.due_date}"



class Complaints(models.Model):
    URGENCY_LEVELS = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical")
    ]

    userregid = models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    complaint_number = models.IntegerField(default=0)
    complainttype = models.CharField(max_length=250)
    stateid = models.ForeignKey(State, on_delete=models.CASCADE)
    noc = models.CharField(max_length=250)
    complaindetails = models.TextField(blank=True)
    compfile = models.ImageField(upload_to='media/doc_file')
    complaintdate_at = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(blank=True)

    urgency = models.CharField(max_length=10, choices=URGENCY_LEVELS, default="Medium")
    assigned_days = models.IntegerField(default=0)
    due_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=250, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    resolved_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='resolved_complaints',
        limit_choices_to={'user_type': 3}  # Optional: only allow staff users to be selected
    )


    def save(self, *args, **kwargs):
        urgency_days = {
            "Low": 10,
            "Medium": 7,
            "High": 5,
            "Critical": 1  
        }

        self.assigned_days = urgency_days.get(self.urgency, 0)

        # Ensure complaintdate_at is set before calculating due date
        if not self.complaintdate_at:
            self.complaintdate_at = now()  # Fix: Use timezone-aware now()

        # Calculate due date
        self.due_date = (self.complaintdate_at + timedelta(days=self.assigned_days)).date()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Complaint {self.complaint_number} - {self.urgency} - Due {self.due_date}"



class ComplaintRemark(models.Model):
    comp_id_id = models.ForeignKey(Complaints, on_delete=models.CASCADE)
    remark = models.TextField(blank=True)
    status = models.CharField(max_length=250,default=0)
    remarkdate = models.DateTimeField(auto_now_add=True)


#lets creat