import os
from django.db import models

# Create your models here.

class Voter(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()
    dob = models.DateField()
    reg_date = models.DateField()
    party = models.TextField()
    precinct_number = models.TextField()
    
    voted_state = models.BooleanField()
    voted_town_21 = models.BooleanField()
    voted_primary = models.BooleanField()
    voted_general = models.BooleanField()
    voted_town_23 = models.BooleanField()
    
    voter_score = models.IntegerField()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.dob}, {self.street_number} {self.street_name}, {self.zip_code}, {self.party}'
    
    def get_year(self):
        # print(self.dob.year)
        return self.dob.year

def load_data():
        Voter.objects.all().delete()
        filename = 'newton_voters.csv'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        f = open(file_path)
        f.readline()
        
        for line in f:
            # row = f.readline().strip()
            fields = line.split(',')
            try:
                last_name=fields[1].strip()
                first_name=fields[2].strip()
                street_number=fields[3].strip()
                street_name=fields[4].strip()
                apartment_number=fields[5].strip()
                zip_code=fields[6].strip()
                dob=fields[7].strip()
                reg_date=fields[8].strip()
                party=fields[9].strip()
                precinct_number=fields[10].strip()
                voted_state=fields[11].strip().lower() in ['true']
                voted_town_21=fields[12].strip().lower() in ['true']
                voted_primary=fields[13].strip().lower() in ['true']
                voted_general=fields[14].strip().lower() in ['true']
                voted_town_23=fields[15].strip().lower() in ['true']
                voter_score=fields[16].strip()
                voter = Voter(
                        last_name=last_name,
                        first_name=first_name,
                        street_number=street_number,
                        street_name=street_name,
                        apartment_number=apartment_number,
                        zip_code=zip_code,
                        dob=dob,
                        reg_date=reg_date,
                        party=party,
                        precinct_number=precinct_number,
                        voted_state=voted_state,
                        voted_town_21=voted_town_21,
                        voted_primary=voted_primary,
                        voted_general=voted_general,
                        voted_town_23=voted_town_23,
                        voter_score=voter_score
                    )
                voter.save()
                print(f'created voter: {voter}')
            except:
                print(f"Skipped: {fields}")
        print(f'Done. Created {len(Voter.objects.all())} Results.')
                