--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.9 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: client_analytics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client_analytics (
    id integer NOT NULL,
    client_id integer,
    last_activity_date date,
    quizzes_finished_total integer,
    quizzes_score_total numeric(3,2),
    level_id_current integer,
    date_level_upgraded date,
    client_rating numeric(6,2)
);


ALTER TABLE public.client_analytics OWNER TO postgres;

--
-- Name: client_analytics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_analytics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_analytics_id_seq OWNER TO postgres;

--
-- Name: client_analytics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_analytics_id_seq OWNED BY public.client_analytics.id;


--
-- Name: client_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client_info (
    client_id integer NOT NULL,
    tg_id integer NOT NULL,
    username text,
    first_name text,
    last_name text,
    date_reg date,
    email text,
    telephone text,
    language_code text,
    level_id_start integer,
    level_id_target integer
);


ALTER TABLE public.client_info OWNER TO postgres;

--
-- Name: client_info_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_info_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_info_client_id_seq OWNER TO postgres;

--
-- Name: client_info_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_info_client_id_seq OWNED BY public.client_info.client_id;


--
-- Name: dictionary; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dictionary (
    word_id integer NOT NULL,
    word_src text NOT NULL,
    word_rus text NOT NULL,
    other_rus1 text NOT NULL,
    other_rus2 text NOT NULL,
    other_rus3 text NOT NULL,
    cat_id integer,
    lev_id integer
);


ALTER TABLE public.dictionary OWNER TO postgres;

--
-- Name: learned_words; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.learned_words (
    client_id integer NOT NULL,
    word_id integer NOT NULL,
    learned_at date DEFAULT CURRENT_DATE,
    activity_id integer
);


ALTER TABLE public.learned_words OWNER TO postgres;

--
-- Name: dictionary_word_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dictionary_word_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dictionary_word_id_seq OWNER TO postgres;

--
-- Name: dictionary_word_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dictionary_word_id_seq OWNED BY public.dictionary.word_id;


--
-- Name: study_level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.study_level (
    lev_id integer NOT NULL,
    lev_name text NOT NULL
);


ALTER TABLE public.study_level OWNER TO postgres;

--
-- Name: study_levels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.study_levels (
    level_id integer NOT NULL,
    level_client text,
    level_word text,
    level_category_code text,
    level_group_code text,
    description text,
    weight_value numeric(3,2)
);


ALTER TABLE public.study_levels OWNER TO postgres;

--
-- Name: study_level_lev_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.study_level_lev_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.study_level_lev_id_seq OWNER TO postgres;

--
-- Name: study_level_lev_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.study_level_lev_id_seq OWNED BY public.study_level.lev_id;


--
-- Name: word_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.word_category (
    cat_id integer NOT NULL,
    cat_name text NOT NULL
);


ALTER TABLE public.word_category OWNER TO postgres;

--
-- Name: word_category_cat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.word_category_cat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.word_category_cat_id_seq OWNER TO postgres;

--
-- Name: word_category_cat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.word_category_cat_id_seq OWNED BY public.word_category.cat_id;


--
-- Name: client_analytics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_analytics ALTER COLUMN id SET DEFAULT nextval('public.client_analytics_id_seq'::regclass);


--
-- Name: client_info client_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_info ALTER COLUMN client_id SET DEFAULT nextval('public.client_info_client_id_seq'::regclass);


--
-- Name: dictionary word_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dictionary ALTER COLUMN word_id SET DEFAULT nextval('public.dictionary_word_id_seq'::regclass);


--
-- Name: study_level lev_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.study_level ALTER COLUMN lev_id SET DEFAULT nextval('public.study_level_lev_id_seq'::regclass);


--
-- Name: word_category cat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.word_category ALTER COLUMN cat_id SET DEFAULT nextval('public.word_category_cat_id_seq'::regclass);


--
-- Data for Name: client_analytics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client_analytics (id, client_id, last_activity_date, quizzes_finished_total, quizzes_score_total, level_id_current, date_level_upgraded, client_rating) FROM stdin;
1	1	2025-05-15	3	1.00	\N	2025-05-15	3.30
\.


--
-- Data for Name: client_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client_info (client_id, tg_id, username, first_name, last_name, date_reg, email, telephone, language_code, level_id_start, level_id_target) FROM stdin;
1	216238348	nikolay_mazur	Nikolay	Mazur	2025-05-15	\N	\N	en	\N	\N
\.


--
-- Data for Name: dictionary; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dictionary (word_id, word_src, word_rus, other_rus1, other_rus2, other_rus3, cat_id, lev_id) FROM stdin;
1	la falda	юбка	брюки	платье	шорты	3	2
2	alegría	радость	печаль	злость	спокойствие	7	2
3	el tren	поезд	машина	автобус	метро	6	1
4	los pantalones	брюки	штаны	панталоны	комбинезон	3	2
5	la camisa	рубашка	блузка	топ	туника	3	2
6	la camiseta	футболка	майка	лонгслив	топ	3	1
7	el vestido	платье	туника	комбинезон	сарафан	3	1
8	los pantalones cortos	шорты	бермуды	плавки	бриджи	3	2
9	el abrigo	пальто	плащ	куртка	накидка	3	3
10	la chaqueta	пиджак	жакет	блейзер	куртка	3	2
11	el jersey	свитер	джемпер	толстовка	водолазка	3	2
12	la bufanda	шарф	платок	горжетка	накидка	3	2
13	el sombrero	шляпа	панама	берет	кепка	3	1
14	el traje	костюм	комплект	ансамбль	форма	3	2
15	los calcetines	носки	гольфы	чулки	следки	3	1
16	los zapatos	ботинки	сапоги	туфли	кроссовки	3	2
17	las zapatillas de casa	тапки	домашние_туфли	шлепанцы	сланцы	3	2
18	las botas	сапоги	ботфорты	валенки	ботинки	3	2
19	las zapatillas de deporte	кроссовки	кеды	слипоны	кроссы	3	1
20	los guantes	перчатки	варежки	рукавицы	митенки	3	3
21	los calzoncillos	нижнее бельё (мужское)	трусы	боксеры	плавки	3	2
22	las bragas	нижнее бельё (женское)	лифчик	трусы	боди	3	2
23	el humano	человек	личность	индивид	существо	1	1
24	el perro	собака	пёс	щенок	псина	1	1
25	el gato	кошка	кот	котёнок	пушистик	1	1
26	el pájaro	птица	пташка	пернатое	воробей	1	1
27	el pez	рыба	рыбка	окунь	карась	1	2
28	el conejo	кролик	заяц	зверёк	питомец	1	2
29	la serpiente	змея	гадюка	уж	рептилия	1	2
30	el león	лев	царь_зверей	хищник	барс	1	1
31	el elefante	слон	гигант	животное	тяжеловес	1	1
32	el caballo	лошадь	конь	пегас	жеребец	1	1
33	la oveja	овца	ягнёнок	баран	животное	1	2
34	el mono	обезьяна	примат	шимпанзе	мартышка	1	2
35	el perrito	щенок	собачка	малютка	питомец	1	2
36	el gatito	котёнок	кошечка	малыш	пушистик	1	2
37	la jirafa	жираф	длинношеее	животное	травоядное	1	1
38	el burro	осёл	ишак	животное	тягловая_скотина	1	3
39	el ratón	мышь	грызун	крыса	питомец	1	3
40	el brazo	рука	кисть	ладонь	конечность	10	1
41	la pierna	нога	ступня	конечность	бедро	10	1
42	la fruta	фрукт	ягода	плод	лакомство	2	1
43	la verdura	овощи	зелень	плоды	овощные_культуры	2	1
44	la patata	картошка	картофель	клубень	овощ	2	1
45	la ensalada	салат	зелень	закуска	смесь	2	1
46	el autobús	автобус	маршрутка	автофургон	троллейбус	6	1
47	el taxi	такси	таксомотор	машина	транспорт	6	1
48	la casa	дом	жилище	коттедж	здание	9	1
49	el piso	квартира; этаж	апартаменты	жильё	помещение	9	2
50	el balcón	балкон	терраса	лоджия	веранда	9	2
51	la planta	растение	цветок	зелень	дерево	8	1
52	el salón	гостиная	зал	комната	приёмная	9	2
53	el sofá	диван	софа	канапе	лежак	9	2
54	el dormitorio	спальня	комната	опочивальня	будуар	9	2
55	el árbol	дерево	растение	дуб	сосна	8	1
56	la habitación	комната	помещение	кабинет	палата	9	2
57	el baño	туалет; ванная комната	уборная	санузел	душевая	9	2
58	la cocina	кухня; печка	кухонное_помещение	плита	место_готовки	9	2
59	el horno	духовка	печь	жаровня	шкаф	9	2
60	el microondas	микроволновка	микроволновая_печь	разогреватель	печка	9	3
61	la nevera	холодильник	морозильник	камера	рефрижератор	9	3
62	el jardín	сад	огород	парк	сквер	8	2
63	el camarero	официант	обслуживающий	подающий	работник	5	2
64	la camarera	официантка	подающая	обслуживающая	работница	5	2
65	el periodista	журналист	репортёр	корреспондент	писатель	5	2
66	la periodista	журналистка	репортёрша	корреспондентка	писательница	5	2
67	el médico	врач	доктор	эскулап	медик	5	1
68	la médica	врач	доктор	эскулап	медик	5	1
69	el psicólogo	психолог	психотерапевт	консультант	аналитик	5	2
70	la psicóloga	психолог	психотерапевт	консультант	аналитик	5	2
71	el dentista	зубной врач	стоматолог	дантист	ортодонт	5	1
72	la dentista	зубной врач	стоматолог	дантист	ортодонт	5	1
73	el profesor	учитель	педагог	преподаватель	наставник	5	1
74	la profesora	учительница	педагог	преподавательница	наставница	5	1
75	el escritor	писатель	автор	литератор	сочинитель	5	2
76	la escritora	писательница	авторша	литераторша	сочинительница	5	2
77	bailar	танцевать	плясать	кружиться	вихляться	4	1
78	ir a bailar	пойти танцевать	плясать	двигаться	танцевать	4	2
79	nadar	плавать	нырять	барахтаться	дрейфовать	4	1
80	ir a nadar	пойти плавать	купаться	нырять	плавать	4	2
81	andar	гулять; ходить	прогуливаться	бродить	ходить	4	1
82	ir de paseo	пойти на прогулку	выгуливаться	прохаживаться	прогуливаться	4	2
83	correr	бегать	спринтовать	мчаться	ускоряться	4	1
84	ir a correr	пойти на пробежку	побежать	устроить_забег	устроить_тренировку	4	2
85	salir	выходить; тусоваться	развлекаться	гулять	веселиться	4	2
86	salir a comer	пойти (куда-либо) на обед	пообедать	сходить_на_ланч	перекусить	4	2
87	salir a cenar	пойти (куда-либо) на ужин	поужинать	поесть	сходить_в_ресторан	4	2
88	dormir	спать	дремать	покемарить	засыпать	4	1
89	quedarse	оставаться	задерживаться	дожидаться	находиться	4	3
90	quedarse despierto	не ложиться спать	бодрствовать	не_засыпать	ночевать	4	2
91	quedarse dormido	спать; заснуть	дремать	уснуть	засыпать	4	2
92	irse a casa	идти домой	направляться	возвращаться	брести	4	1
\.


--
-- Data for Name: learned_words; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.learned_words (client_id, word_id, learned_at, activity_id) FROM stdin;
1	51	2025-05-15	\N
1	55	2025-05-15	\N
1	62	2025-05-15	\N
\.


--
-- Data for Name: study_level; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.study_level (lev_id, lev_name) FROM stdin;
1	начальный
2	средний
3	продвинутый
\.


--
-- Data for Name: study_levels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.study_levels (level_id, level_client, level_word, level_category_code, level_group_code, description, weight_value) FROM stdin;
1	a1 — начальный (beginner)	начальный	начальный_a1	начальный	Простые фразы, знакомство, базовые выражения	1.00
2	a2 — элементарный (elementary)	начальный	начальный_a2	начальный	Бытовые выражения, семья, покупки	1.00
3	b1 — средний (intermediate)	средний	средний_b1	средний	Повседневные ситуации, путешествия	1.30
4	b2 — выше среднего (upper-intermediate)	средний	средний_b2	средний	Абстрактные темы, беглая речь	1.30
5	c1 — продвинутый (advanced)	продвинутый	продвинутый_c1	продвинутый	Свободная речь, сложные тексты	1.60
6	c2 — совершенство (proficient)	продвинутый	продвинутый_c2	продвинутый	Понимание всего, точная речь	1.60
\.


--
-- Data for Name: word_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.word_category (cat_id, cat_name) FROM stdin;
1	животные
2	овощи и фрукты
3	одежда
4	глаголы действия
5	профессии
6	транспорт
7	эмоции
8	природа
9	дом и быт
10	части тела
\.


--
-- Name: client_analytics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_analytics_id_seq', 3, true);


--
-- Name: client_info_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_info_client_id_seq', 1, true);


--
-- Name: dictionary_word_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dictionary_word_id_seq', 92, true);


--
-- Name: study_level_lev_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.study_level_lev_id_seq', 3, true);


--
-- Name: word_category_cat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.word_category_cat_id_seq', 10, true);


--
-- Name: client_analytics client_analytics_client_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_analytics
    ADD CONSTRAINT client_analytics_client_id_key UNIQUE (client_id);


--
-- Name: client_analytics client_analytics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_analytics
    ADD CONSTRAINT client_analytics_pkey PRIMARY KEY (id);


--
-- Name: client_info client_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_info
    ADD CONSTRAINT client_info_pkey PRIMARY KEY (client_id);


--
-- Name: client_info client_info_tg_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_info
    ADD CONSTRAINT client_info_tg_id_key UNIQUE (tg_id);


--
-- Name: dictionary dictionary_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dictionary
    ADD CONSTRAINT dictionary_pkey PRIMARY KEY (word_id);


--
-- Name: learned_words learned_words_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learned_words
    ADD CONSTRAINT learned_words_pkey PRIMARY KEY (client_id, word_id);


--
-- Name: study_level study_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.study_level
    ADD CONSTRAINT study_level_pkey PRIMARY KEY (lev_id);


--
-- Name: study_levels study_levels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.study_levels
    ADD CONSTRAINT study_levels_pkey PRIMARY KEY (level_id);


--
-- Name: word_category word_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.word_category
    ADD CONSTRAINT word_category_pkey PRIMARY KEY (cat_id);


--
-- Name: idx_unique_category_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_unique_category_lower ON public.word_category USING btree (lower(cat_name));


--
-- Name: idx_unique_level_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_unique_level_lower ON public.study_level USING btree (lower(lev_name));


--
-- Name: idx_unique_word_src_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_unique_word_src_lower ON public.dictionary USING btree (lower(word_src));


--
-- Name: client_analytics client_analytics_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_analytics
    ADD CONSTRAINT client_analytics_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client_info(client_id);


--
-- Name: client_analytics client_analytics_level_id_current_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_analytics
    ADD CONSTRAINT client_analytics_level_id_current_fkey FOREIGN KEY (level_id_current) REFERENCES public.study_levels(level_id);


--
-- Name: client_info client_info_level_id_start_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_info
    ADD CONSTRAINT client_info_level_id_start_fkey FOREIGN KEY (level_id_start) REFERENCES public.study_levels(level_id);


--
-- Name: client_info client_info_level_id_target_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client_info
    ADD CONSTRAINT client_info_level_id_target_fkey FOREIGN KEY (level_id_target) REFERENCES public.study_levels(level_id);


--
-- Name: dictionary dictionary_cat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dictionary
    ADD CONSTRAINT dictionary_cat_id_fkey FOREIGN KEY (cat_id) REFERENCES public.word_category(cat_id);


--
-- Name: dictionary dictionary_lev_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dictionary
    ADD CONSTRAINT dictionary_lev_id_fkey FOREIGN KEY (lev_id) REFERENCES public.study_level(lev_id);


--
-- Name: learned_words learned_words_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learned_words
    ADD CONSTRAINT learned_words_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.client_activity_log(id);


--
-- Name: learned_words learned_words_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learned_words
    ADD CONSTRAINT learned_words_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client_info(client_id);


--
-- Name: learned_words learned_words_word_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.learned_words
    ADD CONSTRAINT learned_words_word_id_fkey FOREIGN KEY (word_id) REFERENCES public.dictionary(word_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

