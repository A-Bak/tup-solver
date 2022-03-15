limit_big(2).  limit_small(1).
team(1..8).  umpire(1..4).
round(1..14).  last(14).

distance(1, 1, 0). distance(1, 2, 745). distance(1, 3, 665). distance(1, 4, 929). distance(1, 5, 605). distance(1, 6, 521). distance(1, 7, 370). distance(1, 8, 587).
distance(2, 1, 745). distance(2, 2, 0). distance(2, 3, 80). distance(2, 4, 337). distance(2, 5, 1090). distance(2, 6, 315). distance(2, 7, 567). distance(2, 8, 712).
distance(3, 1, 665). distance(3, 2, 80). distance(3, 3, 0). distance(3, 4, 380). distance(3, 5, 1020). distance(3, 6, 257). distance(3, 7, 501). distance(3, 8, 664).
distance(4, 1, 929). distance(4, 2, 337). distance(4, 3, 380). distance(4, 4, 0). distance(4, 5, 1380). distance(4, 6, 408). distance(4, 7, 622). distance(4, 8, 646).
distance(5, 1, 605). distance(5, 2, 1090). distance(5, 3, 1020). distance(5, 4, 1380). distance(5, 5, 0). distance(5, 6, 1010). distance(5, 7, 957). distance(5, 8, 1190).
distance(6, 1, 521). distance(6, 2, 315). distance(6, 3, 257). distance(6, 4, 408). distance(6, 5, 1010). distance(6, 6, 0). distance(6, 7, 253). distance(6, 8, 410).
distance(7, 1, 370). distance(7, 2, 567). distance(7, 3, 501). distance(7, 4, 622). distance(7, 5, 957). distance(7, 6, 253). distance(7, 7, 0). distance(7, 8, 250).
distance(8, 1, 587). distance(8, 2, 712). distance(8, 3, 664). distance(8, 4, 646). distance(8, 5, 1190). distance(8, 6, 410). distance(8, 7, 250). distance(8, 8, 0).
distance(X,Y,D) :- distance(Y,X,D).
max_distance(1380).

plays(1, 5, 1). plays(4, 8, 1). plays(6, 2, 1). plays(7, 3, 1).
plays(1, 6, 2). plays(2, 8, 2). plays(4, 7, 2). plays(5, 3, 2).
plays(1, 4, 3). plays(2, 7, 3). plays(3, 8, 3). plays(5, 6, 3).
plays(3, 7, 4). plays(5, 4, 4). plays(6, 1, 4). plays(8, 2, 4).
plays(3, 4, 5). plays(6, 5, 5). plays(7, 2, 5). plays(8, 1, 5).
plays(2, 3, 6). plays(4, 6, 6). plays(7, 1, 6). plays(8, 5, 6).
plays(1, 8, 7). plays(2, 6, 7). plays(4, 3, 7). plays(7, 5, 7).
plays(1, 7, 8). plays(2, 4, 8). plays(3, 6, 8). plays(5, 8, 8).
plays(3, 2, 9). plays(4, 1, 9). plays(5, 7, 9). plays(6, 8, 9).
plays(2, 1, 10). plays(4, 5, 10). plays(6, 3, 10). plays(8, 7, 10).
plays(2, 5, 11). plays(3, 1, 11). plays(7, 6, 11). plays(8, 4, 11).
plays(1, 2, 12). plays(3, 5, 12). plays(7, 4, 12). plays(8, 6, 12).
plays(1, 3, 13). plays(5, 2, 13). plays(6, 4, 13). plays(7, 8, 13).
plays(4, 2, 14). plays(5, 1, 14). plays(6, 7, 14). plays(8, 3, 14).

% Defines home team as the first of the two teams.
home_team(Home,R) :- plays(Home,Away,R).
% Generating search space, Umpire X moves to the home venue of team Y in round T
% Constrains the umpires movement to 1 move per round
1 { move(X,Y,T) : home_team(Y,T) } 1 :- umpire(X), round(T).
:- move(U1,T,R), move(U2,T,R), U1 != U2.
:- home_team(T,R), round(R), { move(U,T,R) : umpire(U) } 0.
been_to(U,T) :- round(R), move(U,T,R).
:- umpire(U), team(T), not been_to(U,T).

:- move(U,T,R1), move(U,T,R2), R1 < R2, limit_big(B), R2 - R1 + 1 <= B.
officiates(U,Home,R) :- move(U,Home,R).

officiates(U,Away,R) :- move(U,Home,R), plays(Home,Away,R).
:- officiates(U,T,R1), officiates(U,T,R2), R1 < R2, limit_small(S), R2 - R1 + 1 <= S.

moved(U,R,D) :- umpire(U), team(T), round(R), R > 1, move(U,T,R), move(U,Tp,R-1), distance(T,Tp,D).
#minimize { D,U,R : moved(U,R,D) }.

