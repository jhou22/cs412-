from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic import *
from .models import  Voter
from django.db.models import Count
# Create your views here.

import plotly
import plotly.graph_objs as go

class VotersListView(ListView):
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        '''
        if any of these values exist, filter the query set
        '''
        qs = super().get_queryset()
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                qs = qs.filter(party=party)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                qs = qs.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                qs = qs.filter(voted_state=True)
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                qs = qs.filter(voted_town_21=True)
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                qs = qs.filter(voted_primary=True)
        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                qs = qs.filter(voted_general=True)
        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                qs = qs.filter(voted_town_23=True)
        if 'before' in self.request.GET or 'after' in self.request.GET:
            before = self.request.GET['before']
            if not before:
                before = '1900-01-01'
            else:
                before = before + '-01-01'
                
            after = self.request.GET['after']
            if not after:
                after = '2024-01-01'
            else:
                after = after + '-01-01'
            
            qs = qs.filter(dob__range=[after, before])
        
        
        return qs
    
        
class VoterDetailView(DetailView):
    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'
    
class GraphView(ListView):
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'
    def get_queryset(self):
        '''
        filter the query set just like before
        '''
        qs = super().get_queryset()
        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                qs = qs.filter(party=party)
        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                qs = qs.filter(voter_score=voter_score)
        if 'v20state' in self.request.GET:
            v20state = self.request.GET['v20state']
            if v20state:
                qs = qs.filter(voted_state=True)
        if 'v21town' in self.request.GET:
            v21town = self.request.GET['v21town']
            if v21town:
                qs = qs.filter(voted_town_21=True)
        if 'v21primary' in self.request.GET:
            v21primary = self.request.GET['v21primary']
            if v21primary:
                qs = qs.filter(voted_primary=True)
        if 'v22general' in self.request.GET:
            v22general = self.request.GET['v22general']
            if v22general:
                qs = qs.filter(voted_general=True)
        if 'v23town' in self.request.GET:
            v23town = self.request.GET['v23town']
            if v23town:
                qs = qs.filter(voted_town_23=True)
        if 'before' in self.request.GET or 'after' in self.request.GET:
            before = self.request.GET['before']
            if not before:
                before = '1900-01-01'
            else:
                before = before + '-01-01'
                
            after = self.request.GET['after']
            if not after:
                after = '2024-01-01'
            else:
                after = after + '-01-01'
            
            qs = qs.filter(dob__range=[after, before])
        
        return qs

    def get_context_data(self, **kwargs):
        # print("Test")
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        '''
        for each graph, grab all data associated with voter affiliation, birthdate and participation, then display all that in a graph, depending on search
        '''
        
        # get all people for each party, count how many in each party and then show it
        members = {}
        party_list = []
        parties = qs.values('party')
        for p in parties:
            if p.get('party') not in party_list:
                party_list.append(p.get('party'))
                members[p.get('party')] = 1
            else:
                members[p.get('party')] += 1

        x = party_list
        y = list(members.values())

        # creates a pie chart
        fig = go.Pie(labels=x, values=y)
        title_text = f"Voter Affiliation Distribution"
        
        # generates html for pie chart
        graph_voter_affiliation_distribution = plotly.offline.plot(
            {"data": [fig], 
            "layout_title_text": title_text,
            },
        auto_open=False, output_type="div",
        )

        # get the count of all voted people for each election
        elections = [len(qs.filter(voted_state=True)), len(qs.filter(voted_town_21=True)), len(qs.filter(voted_primary=True)), len(qs.filter(voted_general=True)), len(qs.filter(voted_town_23=True)),
        ]
        
        election_list = ['2020 State Election', '2021 Town Election', '2021 Primary Election', '2022 General Election', '2023 Town Election']
        
        x = election_list
        y = elections
        
        # creates bar chart
        fig = go.Bar(x=x, y=y)
        title_text="Voter Participation by Election"
        
        # gets the html for the chart
        graph_voter_participation = plotly.offline.plot(
            {"data": [fig], 
            "layout_title_text": title_text,
            }, auto_open=False, output_type="div",
                                            
        )
        
        # same thing with voter affiliation
        people = {}
        dob_list = []
        dobs = qs.values('dob__year')
        for d in dobs:
            if d.get('dob__year') not in dob_list:
                dob_list.append(d.get('dob__year'))
                people[d.get('dob__year')] = 1
            else:
                people[d.get('dob__year')] += 1

        x = dob_list
        y = list(people.values())
        
        
        # creates bar chart
        fig = go.Bar(x=x, y=y)
        title_text="Voter Distribution by Birth Year"
        
        graph_voter_birth_year_distribution = plotly.offline.plot(
        {"data": [fig], 
        "layout_title_text": title_text,
        }, auto_open=False, output_type="div",
        )
        
        # Adds all newly created charts to context list
        context['graph_affiliation'] = graph_voter_affiliation_distribution
        
        context['graph_participation'] = graph_voter_participation
        
        context['graph_birth_year'] = graph_voter_birth_year_distribution
            
        return context
        