INSERT INTO actress (name) VALUES
('ALICE PREYSSAS'),
('ALEXIANE TORRES'),
('CAMILLE ARRIVÉ'),
('CHLOÉ FROGET'),
('DIANE RENIER'),
('HÉLÈNE BOUTIN'),
('JULIE CAVANNA'),
('LYMIA VITTE'),
('MADISON GOLAZ'),
('LÉNA BRÉBAN');

INSERT INTO scene (scene_number) VALUES
(1),(2),(3),(4),(5);

INSERT INTO avatar (name, actress_id)
VALUES
('BUD',        (SELECT id FROM actress WHERE name = 'ALICE PREYSSAS')),
('CASSIE',     (SELECT id FROM actress WHERE name = 'ALICE PREYSSAS')),
('CILLIAN',    (SELECT id FROM actress WHERE name = 'ALEXIANE TORRES')),
('DUTCH',      (SELECT id FROM actress WHERE name = 'ALEXIANE TORRES')),
('ED',         (SELECT id FROM actress WHERE name = 'CAMILLE ARRIVÉ')),
('MORRIS',     (SELECT id FROM actress WHERE name = 'CAMILLE ARRIVÉ')),
('GOLDWEISER', (SELECT id FROM actress WHERE name = 'CHLOÉ FROGET')),
('TONY',       (SELECT id FROM actress WHERE name = 'CHLOÉ FROGET')),
('FRANCIE',    (SELECT id FROM actress WHERE name = 'DIANE RENIER')),
('JOE',        (SELECT id FROM actress WHERE name = 'DIANE RENIER')),
('ELLEN',      (SELECT id FROM actress WHERE name = 'HÉLÈNE BOUTIN')),
('ÉMILE',      (SELECT id FROM actress WHERE name = 'HÉLÈNE BOUTIN')),
('JIM',        (SELECT id FROM actress WHERE name = 'JULIE CAVANNA')),
('GEORGES',    (SELECT id FROM actress WHERE name = 'LÉNA BRÉBAN')),
('JAKE',       (SELECT id FROM actress WHERE name = 'LYMIA VITTE')),
('NELLIE',     (SELECT id FROM actress WHERE name = 'LYMIA VITTE')),
('STAN',       (SELECT id FROM actress WHERE name = 'LYMIA VITTE')),
('ANNA',       (SELECT id FROM actress WHERE name = 'MADISON GOLAZ')),
('ÉMILIE',     (SELECT id FROM actress WHERE name = 'MADISON GOLAZ')),
('OGELTORPE',  (SELECT id FROM actress WHERE name = 'MADISON GOLAZ'));

INSERT INTO scene_presence (scene_id, avatar_id)
VALUES
((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'BUD')),
((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'BUD')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'BUD')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'CASSIE')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'CASSIE')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'CASSIE')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'CILLIAN')),
((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'CILLIAN')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'CILLIAN')),

((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'DUTCH')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'DUTCH')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'ED')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'ED')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'ED')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'MORRIS')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'MORRIS')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'MORRIS')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'GOLDWEISER')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'GOLDWEISER')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'GOLDWEISER')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'TONY')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'TONY')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'TONY')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'FRANCIE')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'FRANCIE')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'FRANCIE')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'JOE')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'JOE')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'JOE')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'ELLEN')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'ELLEN')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'ELLEN')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'ÉMILE')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'ÉMILE')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'ÉMILE')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'JIM')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'JIM')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'JIM')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'GEORGES')),
((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'GEORGES')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'GEORGES')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'JAKE')),
((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'JAKE')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'JAKE')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'NELLIE')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'NELLIE')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'NELLIE')),

((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'STAN')),
((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'STAN')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'STAN')),

((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'ANNA')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'ANNA')),
((SELECT id FROM scene WHERE scene_number = 5), (SELECT id FROM avatar WHERE name = 'ANNA')),

((SELECT id FROM scene WHERE scene_number = 3), (SELECT id FROM avatar WHERE name = 'ÉMILIE')),

((SELECT id FROM scene WHERE scene_number = 1), (SELECT id FROM avatar WHERE name = 'OGELTORPE')),
((SELECT id FROM scene WHERE scene_number = 2), (SELECT id FROM avatar WHERE name = 'OGELTORPE')),
((SELECT id FROM scene WHERE scene_number = 4), (SELECT id FROM avatar WHERE name = 'OGELTORPE'));