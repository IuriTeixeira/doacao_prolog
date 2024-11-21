%ID para a UI
id(0,joao).
id(1, davi).
id(2, maria).
id(3, ana).
id(4, julia).
id(5, alice).
id(6, pedro).
id(7, laura).
id(8, manuela).
id(9, vitoria).
id(10, manuel).
id(11, jose).
id(12, carlos).
id(13, telma).

%base de conhecimento
tiposanguineo(joao,a).
tiposanguineo(davi,a).
tiposanguineo(maria,a).
tiposanguineo(ana,a).
tiposanguineo(julia,o).
tiposanguineo(alice,a).
tiposanguineo(pedro,a).
tiposanguineo(laura,b).
tiposanguineo(manuela,b).
tiposanguineo(vitoria,b).
tiposanguineo(manuel,o).
tiposanguineo(jose,ab).
tiposanguineo(carlos,ab).
tiposanguineo(telma,o).
fatorrh(joao,+).
fatorrh(davi,+).
fatorrh(maria,-).
fatorrh(ana,-).
fatorrh(julia,+).
fatorrh(alice,+).
fatorrh(pedro,-).
fatorrh(laura,+).
fatorrh(manuela,-).
fatorrh(vitoria,+).
fatorrh(manuel,+).
fatorrh(jose,+).
fatorrh(carlos,-).
fatorrh(telma,-).
peso(joao,75.7).
peso(davi,50).
peso(maria,49).
peso(ana,80).
peso(julia,47).
peso(alice,30).
peso(pedro,20).
peso(laura,54).
peso(manuela,61).
peso(vitoria,70).
peso(manuel,130).
peso(jose,65).
peso(carlos,48).
peso(telma,79).
idade(joao,41).
idade(davi,24).
idade(maria,51).
idade(ana,17).
idade(julia,15).
idade(alice,56).
idade(pedro,10).
idade(laura,18).
idade(manuela,66).
idade(vitoria,12).
idade(manuel,56).
idade(jose,100).
idade(carlos,67).
idade(telma,48).

%compativel
compativel(X,Y) :- tiposanguineo(X,a), tiposanguineo(Y,a).
compativel(X,Y) :- tiposanguineo(X,a), tiposanguineo(Y,ab).
compativel(X,Y) :- tiposanguineo(X,b), tiposanguineo(Y,b).
compativel(X,Y) :- tiposanguineo(X,b), tiposanguineo(Y,ab).
compativel(X,Y) :- tiposanguineo(X,ab), tiposanguineo(Y,ab).
compativel(X,Y) :- tiposanguineo(X,o), tiposanguineo(Y,a).
compativel(X,Y) :- tiposanguineo(X,o), tiposanguineo(Y,b).
compativel(X,Y) :- tiposanguineo(X,o), tiposanguineo(Y,ab).
compativel(X,Y) :- tiposanguineo(X,o), tiposanguineo(Y,o).

%rhcomp
rhcomp(X,Y) :- fatorrh(X,+), fatorrh(Y,+).
rhcomp(X,Y) :- fatorrh(X,-), fatorrh(Y,+).
rhcomp(X,Y) :- fatorrh(X,-), fatorrh(Y,-).

%podedoar
podedoar(X,Y) :- compativel(X,Y), rhcomp(X,Y), idade(X,I), I >= 18, peso(X,P), P > 50, dif(X,Y).