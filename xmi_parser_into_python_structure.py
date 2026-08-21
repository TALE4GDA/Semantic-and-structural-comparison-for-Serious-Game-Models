# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 14:51:10 2026

@author: madeleine.valat
"""

from enum import Enum
from bs4 import BeautifulSoup
from random import choice
import time

t0=time.time()
# from synonymie import clusters,synonymes
clusters,synonymes=[['ildephonse.Learning Object', 'ildephonse.Atomic Learning Object', 'ildephonse.Composite Learning Object', 'ildephonse.Lesson', 'ildephonse.Course', 'avilapesantez.Teaching Objectives', 'avilapesantez.Learning Tools', 'avilapesantez.Pedagogical and Didactical Aspect', 'avilapesantez.Playful Pedagogical Strategy', 'avilapesantez.Active Learning', 'avilapesantez.Praxis Educational', 'avilapesantez.Sociocultural Learning Theory', 'avilapesantez.Learning Theory', 'avilapesantez.Game According to Educational Goals', 'avilapesantez.Learning Disorders', 'avilapesantez.Motivating and Stimulating Learning', 'avilapesantez.Learning Behaviour', 'avilapesantez.Control of Pedagogical Quality in the Game', 'Carvalho.Learning Action', 'Carvalho.Learning Tool', 'Carvalho.Experience Points', 'Carvalho.Learning Action Category', 'Carvalho.Learning Tool Category', 'Carvalho.Student diary', 'Carvalho.Textbooks', 'Carvalho.Kolb’s experiential learning cycle', 'Carvalho.Learning how to learn', 'Carvalho.Review lesson', "Carvalho.Gagne's Nine Events of Instruction", 'Carvalho.Inform learner of objective', 'Carvalho.Provide learning guidance', 'Carvalho.Learning Activity', 'DeTroyer.Pedagogical theory', 'gps.educative', 'gps.education', 'gps.students', 'marne.Pedagogical Objectives', 'marne.Pedagogical Expertise', 'sglom.Educational', 'sglom.learning resource type'], ['ildephonse.Gamification', 'Amory.Writing', 'avilapesantez.Specification Document', 'avilapesantez.Document Specification', 'avilapesantez.Specification Document', 'avilapesantez.Identity', 'avilapesantez.Character Characteristics', 'Carvalho.give Category', 'Carvalho.Non-playing characters', 'Carvalho.Guide character', 'Carvalho.Identify', 'Carvalho.Label', 'Carvalho.Name', 'Carvalho.Recognize', 'Carvalho.Write', 'Carvalho.Generalize', 'Carvalho.Translate', 'Carvalho.Classify', 'Carvalho.Translate', 'Carvalho.Categorize', 'Carvalho.Identify', 'Carvalho.Subdivide', 'Carvalho.Textual information', 'Carvalho.Classifications', 'Carvalho.Texts', 'Carvalho.Bloom’s Taxonomy Cognitive domain', 'Carvalho.Bloom’s Taxonomy Affective domain', 'Carvalho.Bloom’s Taxonomy Psychomotor domain', 'Carvalho.Fink’s Taxonomy', 'Carvalho.Help text', 'Carvalho.Type', 'Carvalho.category', 'DeTroyer.name', 'DeTroyer.Annotation Brick', 'DeTroyer.title', 'DeTroyer.Non Playable Character', 'DeTroyer.Pedagogical annotation', 'gps.ecology', 'lmgm.Identify', 'lmgm.Generalisation/Discrimination', 'Mariais.title', 'Mariais.title', 'Mariais.title', 'mecanicartes.name', 'playtil.Type', 'sglom.Annotation', 'sglom.Classification', 'sglom.type', 'sglom.Taxon Path', 'sglom.Taxon', 'sglom.id', 'sglom.keyword', 'sglom.Identifier', 'sglom.General', 'sglom.identifier', 'sglom.title', 'sglom.language', 'sglom.keyword', 'sglom.Meta-metadata', 'sglom.identifier', 'sglom.metadata schema', 'sglom.language', 'sglom.format', 'sglom.type', 'sglom.name'], ['ildephonse.Assessment', 'ildephonse.Feedback', 'Amory.Multiple views', 'Amory.Reflection', 'Amory.Complex', 'Amory.Mathematical', 'Amory.Computational', 'avilapesantez.Evaluation Design', 'avilapesantez.Feedback', 'avilapesantez.Factors', 'avilapesantez.Features', 'avilapesantez.Aspects', 'Carvalho.Zero-sum/Non-zero-sum', 'Carvalho.Analyzing', 'Carvalho.Evaluating', 'Carvalho.Observe', 'Carvalho.Relate', 'Carvalho.Relate', 'Carvalho.Summarize', 'Carvalho.Calculate', 'Carvalho.Examine', 'Carvalho.Analyze', 'Carvalho.Deduce', 'Carvalho.Examine', 'Carvalho.Investigate', 'Carvalho.Assess', 'Carvalho.Critique', 'Carvalho.Decide', 'Carvalho.Determine', 'Carvalho.Evaluate', 'Carvalho.Review', 'Carvalho.Value', 'Carvalho.Weigh', 'Carvalho.Add to', 'Carvalho.Devise', 'Carvalho.Other', 'Carvalho.Conclusions', 'Carvalho.Reports', 'Carvalho.Summaries', 'Carvalho.Events', 'Carvalho.Self-evaluations', 'Carvalho.Values', 'Carvalho.Analyzing', 'Carvalho.Evaluating', 'Carvalho.Receiving phenomena', 'Carvalho.Responding to phenomena', 'Carvalho.Valuing', 'Carvalho.Internalizing values', 'Carvalho.Guided response', 'Carvalho.Complex overt response', 'Carvalho.Reflective observation', 'Carvalho.Support recovery from errors', 'Carvalho.Provide feedback', 'Carvalho.Attributes', 'Carvalho.Feedback', 'DeTroyer.attributes', 'gps.subjective', 'gps.Scope', 'lmgm.Reflect/Discuss', 'lmgm.Analyse', 'lmgm.Feedback', 'lmgm.Assessment', 'lmgm.Observation', 'lmgm.Shadowing', 'lmgm.Feedback', 'lmgm.Assessment', 'lmgm.Analysing', 'lmgm.Evaluating', 'Mariais.Properties', 'Mariais.properties', 'Mariais.Component', 'Mariais.Debrief', 'marne.Decorum', 'mecanicartes.Majority', 'mecanicartes.Calculation', 'mecanicartes.Observation', 'playtil.Numeric', 'playtil.Supportless', 'playtil.Support', 'sglom.coverage', 'sglom.Contribute', 'sglom.contribute'], ['ildephonse.Activity', 'Amory.Gestures', 'Amory.Flow', 'Amory.Activity-based', 'Amory.Manipulation', 'Amory.Reflex', 'avilapesantez.Activity Theory', 'avilapesantez.Reflexibility', 'Carvalho.action', 'Carvalho.action', 'Carvalho.Manipulation', 'Carvalho.Movement', 'Carvalho.Manipulate Gravity', 'Carvalho.Move', 'Carvalho.Rotate', 'Carvalho.Alternating turns', 'Carvalho.Perform task within allotted time', 'Carvalho.Imitate', 'Carvalho.Reproduce', 'Carvalho.Demonstrate', 'Carvalho.Experiment', 'Carvalho.Manipulate', 'Carvalho.Perform action/task', 'Carvalho.Invent', 'Carvalho.Demonstrations', 'Carvalho.Experiments', 'Carvalho.Inventions', 'Carvalho.Active experimentation', 'Carvalho.Human dimension', 'Carvalho.Demonstrate', 'Carvalho.Present the stimulus', 'Carvalho.Elicit performance', 'Carvalho.action', 'DeTroyer.Action', 'gps.physical', 'gps.scientific research', 'lmgm.Experimentation', 'lmgm.Action/Task', 'lmgm.Demonstration', 'lmgm.Imitation', 'lmgm.Behavioural Momentum', 'lmgm.Movement', 'Mariais.Activity Area', 'mecanicartes.Moving', 'mecanicartes.Dexterity', 'mecanicartes.Speed', 'sglom.resulting activity'], ['ildephonse.Scenario', 'Amory.Gender-inclusive', 'Amory.Short-term', 'Amory.Long-term', 'Amory.Gender', 'avilapesantez.Phase', 'avilapesantez.Analysis Phase', 'avilapesantez.Risk Analysis', 'avilapesantez.Development Phase', 'avilapesantez.Evaluation Phase', 'avilapesantez.Maintenance', 'avilapesantez.Continuous Improvement Plan', 'avilapesantez.Player Age', 'avilapesantez.Scenario Characteristics', 'Carvalho.Plan/Strategy', 'Carvalho.Lives', 'Carvalho.Achievements', 'Carvalho.Progress bars', 'Carvalho.Status levels', 'Carvalho.Levels', 'Carvalho.Achievement', 'Carvalho.Success level', 'Carvalho.Reach narrative end', 'Carvalho.Be the first to reach the end', 'Carvalho.Predict', 'Carvalho.Complete', 'Carvalho.Defend', 'Carvalho.Forecast', 'Carvalho.Hypothesize', 'Carvalho.Imagine', 'Carvalho.Plan', 'Carvalho.Predict', 'Carvalho.Propose', 'Carvalho.Speculations', 'Carvalho.Forecasts', 'Carvalho.Stress importance', 'Carvalho.Suggest improvements', 'Carvalho.Satisfaction', 'lmgm.deepth', 'lmgm.Planning', 'lmgm.Hypothesis', 'lmgm.Protégé Effect', 'lmgm.Status', 'lmgm.Strategy/Planning', 'lmgm.Progression', 'Mariais.Scenario', 'marne.Problems and Progression', 'mecanicartes.level', 'mecanicartes.Planning', 'sglom.typical age range', 'sglom.progress indicators', 'sglom.aggregation level', 'sglom.Life cycle', 'sglom.status', 'sglom.duration'], ['ildephonse.Story', 'Amory.Narrative spaces', 'Amory.Story', 'Amory.Drama', 'Amory.Backstory', 'Amory.Narrative', 'avilapesantez.Narrative', 'Carvalho.Cut scenes', 'Carvalho.Story (text)', 'Carvalho.Narrative', 'Carvalho.Get acquainted with story', 'Carvalho.Dramatizing', 'Carvalho.Dramas', 'Carvalho.Dramatizations', 'Carvalho.Story', 'Carvalho.Tell story', 'Carvalho.Story', 'Carvalho.Narrative (aesthetics)', 'DeTroyer.Story', 'DeTroyer.Scene', 'lmgm.Cut Scenes/Story', 'Mariais.Play a scene', 'mecanicartes.Storytelling'], ['ildephonse.Topic', 'Amory.Core Concept', 'Amory.Relevance', 'Amory.Logical', 'Amory.Abstract Interface', 'Amory.Indirect', 'Carvalho.Entity', 'Carvalho.Understanding', 'Carvalho.Define', 'Carvalho.Describe', 'Carvalho.Compare', 'Carvalho.Describe', 'Carvalho.Distinguish', 'Carvalho.Explain', 'Carvalho.Interpret', 'Carvalho.Objectify', 'Carvalho.Interpret', 'Carvalho.Compare', 'Carvalho.Contrast', 'Carvalho.Differentiate', 'Carvalho.Distinguish', 'Carvalho.Explain', 'Carvalho.Separate', 'Carvalho.Justify', 'Carvalho.Originate', 'Carvalho.Analogies', 'Carvalho.Definitions', 'Carvalho.Understanding', 'Carvalho.Perception (awareness)', 'Carvalho.Origination', 'Carvalho.Abstract conceptualization', 'Carvalho.Relevance', 'Carvalho.object/motive', 'Carvalho.object/motive', 'Carvalho.Intrinsic', 'Carvalho.Extrinsic', 'Carvalho.object/motive', 'Carvalho.subject', 'Carvalho.Subject', 'Carvalho.Objects', 'DeTroyer.Objective', 'gps.Purpose', 'lmgm.Objectify', 'lmgm.Understanding', 'Mariais.Principle Name', 'Mariais.Present', 'Mariais.presence', 'mecanicartes.description', 'mecanicartes.use context example', 'mecanicartes.Logic', 'playtil.Existing', 'sglom.context', 'sglom.means', 'sglom.description', 'sglom.entity', 'sglom.purpose', 'sglom.source', 'sglom.description', 'sglom.description', 'sglom.description', 'sglom.description', 'sglom.entity', 'sglom.entity'], ['Amory.Serious Game', 'Amory.Game Space', 'Amory.Play', 'Amory.Game rhythm', 'Amory.Game definition', 'avilapesantez.Serious Game', 'avilapesantez.create Serious Game', 'avilapesantez.Serious Game Design', 'avilapesantez.User/Player Profile', 'avilapesantez.Game Mechanisms', 'avilapesantez.Game Programming', 'avilapesantez.Game Integration', 'avilapesantez.Epistemic Game Theory', 'avilapesantez.Game Genre', 'avilapesantez.Reasonable Game Narrative', 'avilapesantez.Game Rules According to Players', 'avilapesantez.Game Complexity', 'avilapesantez.Duration of Activities Within the Game', 'avilapesantez.Structure of Game Levels', 'avilapesantez.Player-centered Actions', 'avilapesantez.Gamer Expectations', 'avilapesantez.Gamer Satisfaction', 'avilapesantez.Gamer Motivation', 'avilapesantez.Game Feedback', 'avilapesantez.Participation in the Game with Other Family Members', 'avilapesantez.Attractive and Fun Game Features', 'avilapesantez.Technology Platform According to Game Needs', 'avilapesantez.Game Support Utility', 'Carvalho.Gaming Tool', 'Carvalho.Gaming Action Category', 'Carvalho.Advance Game Period', 'Carvalho.Serious Game', 'Carvalho.Game modes', 'Carvalho.Game master / referee', 'Carvalho.Multiplayer', 'Carvalho.Game Period', 'Carvalho.Infinite gameplay', 'Carvalho.Meta-game', 'Carvalho.Video Game Score', 'Carvalho.Be the last player standing', 'Carvalho.Configure game', 'Carvalho.Gaming Action', 'Carvalho.Gaming Activity', 'Carvalho.Serious Game Component', 'Carvalho.Gaming Tool Category', 'Carvalho.Segmentation of gameplay', 'DeTroyer.Game Move', 'DeTroyer.Gameplay annotation', 'gps.Serious Game', 'gps.Gameplay', 'gps.play-based', 'gps.game-based', 'lmgm.Infinite Gameplay', 'lmgm.Game Mechanic', 'lmgm.Game Turns', 'lmgm.Metagame', 'Mariais.Game principles', 'marne.Serious Game', 'marne.Game Design Expertise', 'mecanicartes.Serious Game', 'playtil.Serious Game', 'playtil.Escape Game', 'playtil.Gameplay', 'sglom.Serious Game Learning Object Metadata Schema', 'sglom.gaming experience required', 'sglom.Entertainment Software Rating Board rating', 'sglom.game type', 'sglom.game genre', 'sglom.Gameplay', 'sglom.multiplayer value'], ['Amory.Social Space', 'Amory.Elements Space', 'Amory.Problem Space', 'Amory.Actors Space', 'Amory.Accomodation', 'Amory.Concrete Interface', 'avilapesantez.Architecture', 'avilapesantez.Constructionist Theory', 'Carvalho.Objects 2D/3D space', 'Carvalho.Grids', 'Carvalho.Tiles', 'Carvalho.Position in space', 'Carvalho.Concrete experience', 'Carvalho.Scaffold', 'DeTroyer.Brick', 'DeTroyer.Regular Brick', 'DeTroyer.Control Brick', 'DeTroyer.Scenario Brick', 'DeTroyer.Choice brick', 'DeTroyer.Order-independant Brick', 'DeTroyer.Concurrence Brick', 'DeTroyer.Sequence Brick', 'lmgm.breadth', 'lmgm.Tiles/Grids', 'Mariais.group size', 'Mariais.Cloackroom', 'Mariais.group size', 'Mariais.Room', 'mecanicartes.Rock-paper-scissors', 'playtil.Construction', 'sglom.size'], ['Amory.Visualization Space', 'Amory.Plot', 'Amory.Fun', 'Amory.Graphics', 'Amory.Sounds', 'Amory.Visual', 'Amory.Visualization', 'Carvalho.Avatars', 'Carvalho.Draw', 'Carvalho.Outline', 'Carvalho.Visualize', 'Carvalho.Illustrate', 'Carvalho.Show', 'Carvalho.Graphical information', 'Carvalho.Multimedia', 'Carvalho.Art', 'Carvalho.Cartoons', 'Carvalho.Diagrams', 'Carvalho.Displays', 'Carvalho.Graphics', 'Carvalho.Graphs', 'Carvalho.Illustrations', 'Carvalho.Animation', 'Carvalho.Films', 'Carvalho.Media presentations', 'Carvalho.Recordings', 'Carvalho.Songs', 'Carvalho.Television programs', 'Carvalho.Videos', 'Carvalho.Outlines', 'Carvalho.Sculptures', 'DeTroyer.icon', 'gps.culture and arts', 'gps.entertainment', 'mecanicartes.Drawing', 'mecanicartes.Figurines'], ['Amory.Computer Mediated Communication', 'Amory.Social Network Analysis', 'Amory.Communication', 'Amory.Network', 'avilapesantez.Communication', 'Carvalho.Teleport', 'Carvalho.Leaderboards', 'Carvalho.Warning messages', 'Carvalho.Social Network Score', 'Carvalho.Advertise', 'Carvalho.Bulletin boards', 'Carvalho.Editorials', 'Carvalho.Magazine articles', 'Carvalho.Newspapers', 'Carvalho.Posters', 'Carvalho.Warning messages', 'gps.Message Broadcasting', 'gps.advertising', 'lmgm.Virality', 'mecanicartes.Board', 'playtil.Board'], ['Amory.Literacy', 'Amory.Conflict', 'Amory.Conversation', 'Amory.Reading', 'Amory.Speaking', 'Amory.Dialogue', 'Carvalho.Watch/Listen To/Read Information', 'Carvalho.Watch/Listen To/Read Story', 'Carvalho.Read', 'Carvalho.Recite', 'Carvalho.Tell', 'Carvalho.Discuss', 'Carvalho.Paraphrase', 'Carvalho.Put into own words', 'Carvalho.Argue', 'Carvalho.Debate', 'Carvalho.Discuss', 'Carvalho.Debates', 'Carvalho.Group discussions', 'Carvalho.Speech', 'Carvalho.Arguments', 'Carvalho.Poems', 'Carvalho.Discussion', 'DeTroyer....', 'DeTroyer....', 'DeTroyer....', 'Mariais.Debate', 'mecanicartes.Confrontation'], ['Amory.Memory', 'Amory.Authentic', 'Amory.Critical thinking', 'Amory.Emotive', 'Amory.Authentic learning', 'avilapesantez.Cognitive Behaviour Theory', 'avilapesantez.Motivation Theory', 'avilapesantez.Psychological Needs', 'avilapesantez.Cognitive Development', 'Carvalho.Gifts', 'Carvalho.Remembering', 'Carvalho.Memorize', 'Carvalho.Recall', 'Carvalho.Restate', 'Carvalho.Estimate', 'Carvalho.Remembering', 'Carvalho.Caring', 'Carvalho.Repetition', 'Carvalho.ARCS (Attention-Relevance-Confidence-Satisfaction) Model of Motivational Design', 'Carvalho.Gain attention', 'Carvalho.Stimulate recall of prior learning', 'Carvalho.Enhance retention and transfer', 'Carvalho.Attention', 'Carvalho.Confidence', 'gps.persuasive', 'gps.mental', 'lmgm.Thinking Skill', 'lmgm.Motivation', 'lmgm.Repetition', 'lmgm.Urgent Optimism', 'lmgm.Realism', 'lmgm.Retention', 'Mariais.Receiving recognition', 'mecanicartes.Memorizing', 'playtil.Psychomotor', 'playtil.Affective', 'playtil.Cognitive', 'sglom.replayability', 'sglom.kind'], ['Amory.Motor', 'Amory.Model-building', 'Amory.Tools', 'avilapesantez.User Experience', 'avilapesantez.Design Phase', 'avilapesantez.Patterns Design', 'avilapesantez.Design Prototype', 'avilapesantez.Application Prototype', 'avilapesantez.User Experience', 'avilapesantez.Interface Aesthetics', 'avilapesantez.Flexibility of Use of the Technological Tool', 'Carvalho.tool', 'Carvalho.tool', 'Carvalho.tool', 'Carvalho.Design', 'Carvalho.Learn to use interface', 'Carvalho.Build model', 'Carvalho.Design', 'Carvalho.Simulator', 'Carvalho.Models', 'Carvalho.Simulators', 'lmgm.Learning Mechanic', 'lmgm.Simulation', 'lmgm.Design/Editing', 'lmgm.Simulate/Response', 'marne.Domain Simulation', 'marne.Interactions with the Simulation', 'mecanicartes.Mechanic', 'mecanicartes.Mechanic Name', 'mecanicartes.Drafting', 'sglom.interactive type', 'sglom.intended end user role'], ['Amory.Challenges', 'Amory.Puzzlement', 'Amory.Challenges-puzzles-quests', 'avilapesantez.Identification of the Problem', 'avilapesantez.Issues', 'Carvalho.Ask Questions', 'Carvalho.Answer Questions/Trivia', 'Carvalho.Challenges', 'Carvalho.Puzzles', 'Carvalho.Quest / Problem', 'Carvalho.Solve puzzle', 'Carvalho.Complete quest', 'Carvalho.Complete side quests', 'Carvalho.Solve', 'Carvalho.Problem-solving', 'Carvalho.Questionnaires', 'Carvalho.Surveys', 'Carvalho.Challenge', 'Carvalho.Problems', 'Carvalho.Puzzles', 'Carvalho.Present problem', 'Carvalho.Present quiz', 'Carvalho.Show similar problems', 'Carvalho.Challenge', 'Carvalho.Questions and answers', 'lmgm.Question and Answers', 'lmgm.Questions and Answers', 'Mariais.Rising to an individual challenge', 'sglom.difficulty'], ['Amory.Engagement', 'Amory.Interaction', 'Amory.Relationships', 'Amory.Democracy', 'Amory.Social capital', 'Amory.Social collaboration', 'avilapesantez.Participatory Strategy', 'avilapesantez.Collaborative Environment', 'avilapesantez.Interactivity', 'avilapesantez.Participatory/Collaborative Context', 'Carvalho.Own', 'Carvalho.State', 'Carvalho.Interaction', 'Carvalho.Organizations', 'Carvalho.Organization', 'gps.state and governement', 'gps.healthcare', 'gps.corporate', 'gps.religious', 'gps.politics', 'gps.humanitarian', 'gps.Public', 'gps.general public', 'lmgm.Accountability', 'lmgm.Ownership', 'lmgm.Participation', 'lmgm.Responsibility', 'lmgm.Collaboration', 'lmgm.Cooperation', 'lmgm.Ownership', 'lmgm.Pavlovian Interactions', 'lmgm.Cooperation', 'lmgm.Collaboration', 'Mariais.Losing control', 'Mariais.Acting collectively', 'Mariais.Group constitution area', 'Mariais.group constitution criteria', 'Mariais.Capitalize', 'Mariais.Participants organisation', 'mecanicartes.Cooperation', 'playtil.Management', 'sglom.interactivity level','sglom.interactivity type', 'sglom.Relation', 'sglom.Rights', 'sglom.copyright and other restrictions'], ['Amory.Transformation', 'Amory.Assimilation', 'Amory.Technology', 'avilapesantez.Requirements Specification', 'avilapesantez.Use', 'avilapesantez.Immersion', 'avilapesantez.Appplication of Integration Techniques', 'Carvalho.Customize', 'Carvalho.Destroy', 'Carvalho.Edit', 'Carvalho.Eliminate', 'Carvalho.Remove', 'Carvalho.Select', 'Carvalho.Avoid', 'Carvalho.Evade', 'Carvalho.Use', 'Carvalho.Modifiers', 'Carvalho.Checklists/ Task lists', 'Carvalho.Tasks', 'Carvalho.Maximize performance', 'Carvalho.Maximize score', 'Carvalho.Applying', 'Carvalho.List', 'Carvalho.Select', 'Carvalho.Convert', 'Carvalho.Apply', 'Carvalho.Change', 'Carvalho.Choose', 'Carvalho.Modify', 'Carvalho.Use', 'Carvalho.Take apart', 'Carvalho.Choose', 'Carvalho.Prioritize', 'Carvalho.Recommend', 'Carvalho.Select', 'Carvalho.Recommendations', 'Carvalho.Routines', 'Carvalho.Rules', 'Carvalho.Standards', 'Carvalho.Task list/ checklist', 'Carvalho.Tasks', 'Carvalho.Systems', 'Carvalho.Applying', 'Carvalho.Adaptation', 'Carvalho.Application', 'Carvalho.Integration', 'Carvalho.Checklists', 'Carvalho.Limited set of choices', 'Carvalho.Rules', 'DeTroyer.Change Objective', 'DeTroyer.Method', 'lmgm.Pareto Optimal', 'lmgm.Appointment', 'lmgm.Applying', 'Mariais.Criterion', 'Mariais.criteria', 'Mariais.Function', 'Mariais.Consult', 'Mariais.Select', 'marne.Conditions of Use', 'playtil.Modified', 'playtil.Turned Away', 'sglom.entry', 'sglom.entry', 'sglom.entry', 'sglom.version', 'sglom.entry', 'sglom.Technical', 'sglom.Requirements', 'sglom.minimum version', 'sglom.maximum version', 'sglom.installation remarks', 'sglom.other platform requirements'], ['Amory.Tacit knowledge', 'Amory.Explicit knowledge', 'Carvalho.Information', 'Carvalho.Information', 'Carvalho.Secrets', 'Carvalho.Complete information', 'Carvalho.Incomplete information', 'Carvalho.Collect information', 'Carvalho.Find more information about', 'Carvalho.Graphed information', 'Carvalho.Information', 'Carvalho.Foundational knowledge', 'gps.informative', 'lmgm.Cascading Information', 'mecanicartes.Secret Identity', 'mecanicartes.Information', 'playtil.Knowledge'], ['Amory.Exploration', 'Amory.Discovery', 'avilapesantez.Resources and Strength Environment', 'avilapesantez.Geographical Location of the Player', 'Carvalho.Manage Resources', 'Carvalho.Traverse', 'Carvalho.Visit', 'Carvalho.Checkpoints', 'Carvalho.Collect resources', 'Carvalho.Reach resources end', 'Carvalho.Find', 'Carvalho.Locate', 'Carvalho.Explore', 'Carvalho.Discover', 'lmgm.Discover', 'lmgm.Explore', 'lmgm.Resource Management', 'lmgm.Communal Discovery', 'mecanicartes.Resource Management', 'playtil.Exploration', 'sglom.Resource', 'sglom.location'], ['Amory.Goal formation', 'Amory.Goal completion', 'avilapesantez.Goal Validation', 'Carvalho.Instructional Goal', 'Carvalho.goal', 'Carvalho.Learning Goal', 'Carvalho.goal', 'Carvalho.Gaming Goal', 'Carvalho.goal', 'Carvalho.Gaming Goal Category', 'Carvalho.Other goals', 'Carvalho.Form/discover goal', 'Carvalho.Complete goal', 'Carvalho.Form goal', 'Carvalho.Learning Goal Category', 'Carvalho.Instructional Goal Category', 'Carvalho.Goal metrics', 'sglom.goals'], ['Amory.Competition', 'Amory.Win/Lose', 'avilapesantez.Rewards', 'Carvalho.Capture', 'Carvalho.Collect', 'Carvalho.Exchange', 'Carvalho.Match', 'Carvalho.Tactical Maneuver', 'Carvalho.Trade Virtual Items', 'Carvalho.Collide', 'Carvalho.Shoot', 'Carvalho.Target', 'Carvalho.Cards', 'Carvalho.Tokens', 'Carvalho.Virtual money', 'Carvalho.Virtual skills', 'Carvalho.Penalties', 'Carvalho.Points', 'Carvalho.Rewards', 'Carvalho.Dice', 'Carvalho.Lottery', 'Carvalho.Random appearances', 'Carvalho.Randomizers', 'Carvalho.Competition', 'Carvalho.Score', 'Carvalho.Cash Score', 'Carvalho.Redeemable Points', 'Carvalho.Karma Points', 'Carvalho.Score', 'Carvalho.Competition', 'Carvalho.Match', 'Carvalho.Judge', 'Carvalho.Rate', 'Carvalho.Combine', 'Carvalho.Court trials', 'Carvalho.Reward good performance', 'Carvalho.Sanction bad performance', 'Carvalho.Multiple chances', 'Carvalho.Penalties', 'Carvalho.Rewards', 'Carvalho.Chance/Randomness', 'Carvalho.Score', 'DeTroyer.Score', 'gps.data exchange', 'gps.Market', 'gps.military', 'lmgm.Competition', 'lmgm.Incentive', 'lmgm.Action Points', 'lmgm.Rewards/Penalties', 'lmgm.Capture/Elimination', 'lmgm.Competition', 'lmgm.Selecting/Collecting', 'lmgm.Tokens', 'Mariais.Being in competition', 'Mariais.Being subject to chance', 'mecanicartes.Card', 'mecanicartes.Combo', 'mecanicartes.Matching', 'mecanicartes.Trading', 'mecanicartes.Auction', 'mecanicartes.Press Your Luck', 'mecanicartes.Bluffing', 'mecanicartes.Bargaining', 'mecanicartes.Cards', 'mecanicartes.Dice', 'mecanicartes.Tokens', 'sglom.cost'], ['Amory.Practice', 'avilapesantez.Teaching Competence', 'avilapesantez.Therapeutic Techniques', 'avilapesantez.Instructional Activities', 'Carvalho.Instructional Action', 'Carvalho.Instructional Tool', 'Carvalho.Enum Gaming Action', 'Carvalho.Obtain Help', 'Carvalho.Enum Gaming Tool', 'Carvalho.Advice and assistance', 'Carvalho.Tips', 'Carvalho.Tutorial', 'Carvalho.Enum Gaming Goal', 'Carvalho.Enum Learning Action', 'Carvalho.Put into practice', 'Carvalho.Enum Learning Tool', 'Carvalho.Tips', 'Carvalho.Enum Learning Goal', 'Carvalho.Mechanism (basic proficiency)', 'Carvalho.Enum Instructional Action', 'Carvalho.Enum Instructional Tool', 'Carvalho.Tips / assistance', 'Carvalho.Enum Instructional Goal', 'Carvalho.Instructional Activity', 'Carvalho.Help', 'DeTroyer.Assist', 'gps.Training', 'gps.professionals', 'lmgm.Tutorial', 'lmgm.Guidance', 'lmgm.Instruction', 'lmgm.Tutorial', 'Mariais.tutoring', 'mecanicartes.Competence', 'mecanicartes.Competence Name', 'playtil.Aimed competences'], ['Amory.Role models', 'Carvalho.Roles', 'Carvalho.Role play', 'DeTroyer.Role-model', 'DeTroyer.Role-modelling', 'lmgm.Role Play', 'Mariais.Playing a role', 'Mariais.roles', 'Mariais.Take a role', 'playtil.Role-playing Game', 'sglom.role', 'sglom.role'], ['avilapesantez.Quality Assurance', 'avilapesantez.Quality Assurance', 'avilapesantez.Quality Assurance', 'avilapesantez.Quality Assurance', 'avilapesantez.Testing', 'avilapesantez.Validation of Input/Output Data', 'Carvalho.See Performance Evaluation', 'Carvalho.Performance meters', 'Carvalho.Performance record', 'Carvalho.Performance record', 'Carvalho.Verify', 'Carvalho.Tests', 'Carvalho.Qualitatively assess performance', 'Carvalho.Quantitatively assess performance', 'Carvalho.Performance measures', 'Carvalho.Practice tests', 'Carvalho.Assess performance', 'DeTroyer.Performance Objective'], ['Carvalho.Time-related', 'Carvalho.Manipulate Time', 'Carvalho.Start/Stop Time', 'Carvalho.Chronometer', 'Carvalho.Time pressure', 'Carvalho.Time', 'Carvalho.Time', 'Carvalho.Deadlines', 'Carvalho.Time', 'lmgm.Time Pressure', 'Mariais.synchronous', 'mecanicartes.Timer', 'sglom.typical learning time', 'sglom.date', 'sglom.date', 'sglom.date'], ['Carvalho.Create', 'Carvalho.Generate', 'Carvalho.Goods', 'Carvalho.Composite Metrics', 'Carvalho.Creating', 'Carvalho.Construct', 'Carvalho.Make', 'Carvalho.Produce', 'Carvalho.Put together', 'Carvalho.Compose', 'Carvalho.Construct', 'Carvalho.Create', 'Carvalho.Formulate', 'Carvalho.Creations', 'Carvalho.Creating', 'Carvalho.Set', 'Carvalho.Present material', 'lmgm.Creating', 'lmgm.Goods/Information', 'Mariais.Produce', 'Mariais.Organize', 'Mariais.Modality', 'Mariais.composition', 'mecanicartes.Material', 'mecanicartes.Material Placement', 'mecanicartes.Set Creation', 'mecanicartes.Material Name', 'mecanicartes.Container', 'mecanicartes.Creative Material', 'mecanicartes.Exotic Material', 'playtil.Created', 'sglom.catalog', 'sglom.catalog', 'sglom.structure', 'sglom.catalog', 'sglom.Or Composite']],[[('course', 0.6351351351351351)], [('identify', 0.5666666666666667)], [('value', 0.4845360824742268)], [('move', 0.9047619047619048)], [('level', 0.4936708860759494), ('plan', 0.4936708860759494)], [('story', 1.303030303030303)], [('separate', 0.4533333333333333)], [('play', 0.8633093525179856)], [('construction', 0.5471698113207547)], [('draw', 2.097560975609756)], [('board', 1.1612903225806452)], [('read', 0.8571428571428571)], [('remember', 0.5925925925925926)], [('design', 0.9215686274509803)], [('challenge', 1.1555555555555554)], [('organisation', 0.4918032786885246), ('organization', 0.4918032786885246)], [('use', 0.7191011235955056)], [('information', 1.1111111111111112)], [('find', 1.1333333333333333)], [('goal', 0.65625)], [('score', 1.043956043956044)], [('tip', 0.8620689655172413)], [('role', 0.9)], [('test', 1.0606060606060606)], [('time', 2.3181818181818183)], [('make', 1.8043478260869565)]]
# print(clusters,synonymes)
t1=time.time()
print(f"Calculs préliminaires effectués en {t1-t0} s")

class Cluster:
    def __init__(self,index,elements,synonym,color):
        self.index=index
        self.synonym=synonym
        self.elements=elements
        self.color=color
    
    def __str__(self):
        print(self.synonym)
        return self.synonym[0][0]
    
    def __repr__(self):
        return str(self)+""

class ElementType(Enum):
    CLASS = 0
    ABSTRACT_CLASS = 1
    INTERFACE = 2
    ENUMERATION = 3
    ENUMERATION_ELEMENT = 4
    METHOD = 5
    ATTRIBUTE = 6

class Element:#can be a Class, a Method/Attribute of a Class, an Interface or an Enumeration class
    def __init__(self,name,model,elementType,cluster):
        self.id=model+"."+name
        self.name=name
        self.model=model
        self.type=elementType
        self.cluster=cluster.synonym
    
    def __str__(self):
        return f"{self.name} : {self.type} ({self.model}) - {self.cluster}"

    def __repr__(self):
        return str(self)
        
class AssociationType(Enum):
    ATTRIBUTE = 0
    METHOD = 1
    HERITAGE = 2
    ENUMERATION = 3
    ASSOCIATION = 4
    NAVIGABLE_ASSOCIATION = 5
    DEPENDENCY = 6
    REALIZATION = 7
    AGGREGATION = 8
    COMPOSITION = 9
    ASSOCIATION_CLASS = 10
        
class Association:
    def __init__(self,name,model,associationType,client,supplier,cluster=None,clientMultiplicity=None,supplierMultiplicity=None):
        self.id=model+"."+str(name)
        self.name=name
        self.model=model
        self.client=client
        self.supplier=supplier
        self.type=associationType
        self.multiplicity={"client":clientMultiplicity,"supplier":supplierMultiplicity}
        self.cluster=None
        if cluster is not None:
            self.cluster=cluster.synonym
    
    def __str__(self):
        return f"{self.client} {self.type} {self.supplier}"
    
    def __repr__(self):
        return str(self)

random_color="#"+''.join([choice('0123456789ABCDEF') for j in range(6)])
clusters=[Cluster(i,clusters[i],synonymes[i],random_color) for i in range(len(clusters))]    

classes=[]
associations=[]

def cluster_of_element(model,term,clusters):
    term_to_search=model+"."+term
    for c in clusters:
        if term_to_search in c.elements:
            return c
    print(model,term)
    raise Exception(f"{term} not found in clusters !")

def add_class(xmi,clusters,model,full_xmi,interface=False):
    name=xmi.get("name")
    if name in ["Map(String,String)","StringToStringMapEntry"]:
        return
    elementType=ElementType.CLASS
    cluster=cluster_of_element(model, name, clusters)
    if interface:
        elementType=ElementType.INTERFACE
    if xmi.get("abstract"):
        elementType=ElementType.ABSTRACT_CLASS
    class_element=Element(name,model,elementType,cluster)
    classes.append(class_element)
    attributes=xmi.findAll("ownedAttribute")
    if attributes!=[]:
        for attr in attributes:
            attr_cluster=cluster_of_element(model,attr.get("name"),clusters)
            attr_element=Element(attr.get("name"),model,ElementType.ATTRIBUTE,attr_cluster)
            classes.append(attr_element)
            associations.append(Association(None, model, AssociationType.ATTRIBUTE, attr_element.id , class_element.id))
    methods=xmi.findAll("ownedOperation")
    if methods!=[]:
        for met in methods:
            met_cluster=cluster_of_element(model,met.get("name"),clusters)
            method_name=met.get("name")+"("
            for param in met.findAll("ownedParameter",direction="in"):
                method_name+=param.get("name")+" : "+param.get("type")+","
            if method_name[-1]==",":
                method_name=method_name[:-1]
            met_return=met.find("ownedParameter",direction="return")
            if met_return:
                method_name+=" : "+met_return.get("type")
            met_element=Element(method_name,model,ElementType.METHOD,met_cluster)
            classes.append(met_element)
            associations.append(Association(None, model, AssociationType.METHOD, met_element.id , class_element.id))
    for parent in xmi.findAll("generalization"):
        id_parent_xmi=parent.get("general")
        def class_parent(tag):
            return tag.get("xmi:id")==id_parent_xmi
        parent=full_xmi.find(class_parent)
        id_parent=model+"."+parent.get("name")
        associations.append(Association(None,model,AssociationType.HERITAGE,class_element.id,id_parent))
    return

def add_interface(xmi,clusters,full_xmi,model):
    return add_class(xmi,clusters,model,full_xmi,interface=True)
    
def add_enumeration(xmi,clusters,model):
    name=xmi.get("name")
    cluster_enum=cluster_of_element(model,name,clusters)
    element_enum=Element(name,model,ElementType.ENUMERATION,cluster_enum)
    classes.append(element_enum)
    possibilities=xmi.findAll("ownedLiteral")
    for poss in possibilities:
        name_poss=poss.get("name")
        cluster_poss=cluster_of_element(model,name_poss,clusters)
        element_poss=Element(name_poss,model,ElementType.ENUMERATION_ELEMENT,cluster_poss)
        classes.append(element_poss)
        associations.append(Association("", model, AssociationType.ENUMERATION, element_poss.id, element_enum.id))
    return

def get_names_end(end1,end2,model,full_xmi):
    try:
        end1_type=end1.get("type")
        end2_type=end2.get("type")
    except:
        end1_type=end1
        end2_type=end2
    def end1_name(tag):
        return tag.get("xmi:id")==end1_type
    def end2_name(tag):
        return tag.get("xmi:id")==end2_type
    end1_id=model+"."+full_xmi.find(end1_name).get("name")
    end2_id=model+"."+full_xmi.find(end2_name).get("name")
    return end1_id,end2_id

def multiplicity(xmi_end):
    mult=""
    lowerValue=xmi_end.get("lowerValue")
    upperValue=xmi_end.get("upperValue")
    if lowerValue or upperValue:
        mult="0.."
    if lowerValue:
        mult=str(lowerValue.get("value"))+".."
    if upperValue:
        mult+=str(upperValue.get("value"))
    else:
        mult+="n"
    return mult
    
def add_association(model,xmi,full_xmi):
    end1,end2=xmi.findAll("ownedEnd")
    end1_id,end2_id=get_names_end(end1,end2,model,full_xmi)
    mult_end1=multiplicity(end1)
    mult_end2=multiplicity(end2)
    name=""
    cluster_association=None
    if xmi.get("name"):
        name=xmi.get("name")
        cluster_association=cluster_of_element(model, name, clusters)
    
    # Gestion de la navigabilite
    if end1.get("isNavigable")=="True":
        id_client=end1_id
        mult_client=mult_end1
        id_supplier=end2_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.NAVIGABLE_ASSOCIATION, id_client, id_supplier,cluster=cluster_association,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end2.get("isNavigable")=="True":
        id_client=end2_id
        mult_client=mult_end2
        id_supplier=end1_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.NAVIGABLE_ASSOCIATION, id_client, id_supplier,cluster=cluster_association,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    #Gestion des aggregations et compositions
    if end1.get("aggregation")=="shared":
        id_client=end2_id
        mult_client=mult_end2
        id_supplier=end1_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.AGGREGATION, id_client, id_supplier,cluster=cluster_association,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end1.get("aggregation")=="composite":
        id_client=end2_id
        mult_client=mult_end2
        id_supplier=end1_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.COMPOSITION, id_client, id_supplier,cluster=cluster_association,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end2.get("aggregation")=="shared":
        id_client=end1_id
        mult_client=mult_end1
        id_supplier=end2_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.AGGREGATION, id_client, id_supplier,cluster=cluster_association,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    elif end2.get("aggregation")=="composite":
        id_client=end1_id
        mult_client=mult_end1
        id_supplier=end2_id
        mult_supplier=mult_end2
        associations.append(Association(name, model, AssociationType.COMPOSITION, id_client, id_supplier,cluster=cluster_association,clientMultiplicity=mult_client,supplierMultiplicity=mult_supplier))
        return
    associations.append(Association(name, model, AssociationType.ASSOCIATION, end1_id, end2_id,cluster=cluster_association,clientMultiplicity=mult_end1,supplierMultiplicity=mult_end2))
    return

def add_association_class(xmi,clusters,model,full_xmi):
    end1,end2=xmi.findAll("ownedEnd")
    id_end1,id_end2=get_names_end(end1, end2, model, full_xmi)
    cluster_class=cluster_of_element(model,xmi.get("name"),clusters)
    mult_end1=multiplicity(end1)
    mult_end2=multiplicity(end2)
    associations.append(Association(xmi.get("name"), model, AssociationType.ASSOCIATION_CLASS, id_end1, id_end2,clientMultiplicity=mult_end1,supplierMultiplicity=mult_end2,cluster=cluster_class))
    return

def add_dependency(xmi,full_xmi,model):
    # print(xmi.get("client"), xmi.get("supplier"), model)
    print(xmi)
    id_client,id_supplier=get_names_end(xmi.get("client"), xmi.get("supplier"), model, full_xmi)
    stereotype=None
    if xmi.find("appliedStereotype") is not None:
        stereotype=xmi.find("appliedStereotype").get("name")
    associations.append(Association(stereotype, model, AssociationType.DEPENDENCY, id_client, id_supplier))
    return 

def add_realization(xmi,full_xmi,model):
    id_client,id_supplier=get_names_end(xmi.get("client"), xmi.get("supplier"), model, full_xmi)
    associations.append(Association("",model,AssociationType.REALIZATION,id_client,id_supplier))
    return

def xmi_into_python_structures(chemin,nom_fichier,clusters):
    print("ici",chemin,nom_fichier,clusters)
    model=nom_fichier
    print("là",chemin+nom_fichier+".xmi")
    with open(chemin+nom_fichier+".xmi",'r',encoding='utf-8') as fichier_entree:
        content=fichier_entree.read()
        soup=BeautifulSoup(content,"xml")
        for element in soup.findAll("packagedElement"):
            if element.get("xmi:type")=="uml:Class":
                add_class(element,clusters,model,soup)
            elif element.get("xmi:type")=="uml:Interface":
                add_interface(element,clusters,soup,model)
            elif element.get("xmi:type")=="uml:Enumeration":
                add_enumeration(element,clusters,model)
            elif element.get("xmi:type")=="uml:Association":
                add_association(model,element,soup)
            elif element.get("xmi:type")=="uml:AssociationClass":
                add_association_class(element,clusters,model,soup)
            elif element.get("xmi:type")=="uml:Dependency":
                add_dependency(element,soup,model)
            elif element.get("xmi:type")=="uml:Realization":
                add_realization(element,soup,model)
            elif element.get("xmi:type") not in ["uml:DataType","uml:PrimitiveType"]:
                raise Exception("Type inconnu : "+element.get("xmi:type"))
    return chemin+nom_fichier+".drawio"

chemin="C:/Users/madeleine.dufrasne/Documents/Recherche/comparaison modèles/modeles/"
fichiers=["Amory","avilapesantez","Carvalho","DeTroyer","gps","ildephonse","lmgm","Mariais","marne","mecanicartes","playtil","sglom"]
# fichiers=["mecanicartes"]

for fichier in fichiers:
    # print(clusters)
    xmi_into_python_structures(chemin,fichier,clusters)#,['#676F35', '#6EF3D1', '#2619C1', '#1A70E7', '#C1B603', '#875A5A', '#3BC9F2', '#56A2E8', '#B6B7CB', '#ED9916', '#DF0BF9', '#7651DC', '#399814'])
# print(classes)
for assoc in associations:
    print(assoc)
        
t2=time.time()
print(f"Calculs effectués en {t2-t1} s")
        
