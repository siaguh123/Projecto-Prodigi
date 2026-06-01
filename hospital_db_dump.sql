--
-- PostgreSQL database dump
--

\restrict rruuR4qjluxkp371xQPjctqdyI3KypbPYzsUAnYE8b2AiNJ13uFNK6pjcmtx4nO

-- Dumped from database version 15.18 (Debian 15.18-1.pgdg13+1)
-- Dumped by pg_dump version 15.18 (Debian 15.18-1.pgdg13+1)

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

ALTER TABLE IF EXISTS ONLY public.triagem DROP CONSTRAINT IF EXISTS triagem_numepis_fkey;
ALTER TABLE IF EXISTS ONLY public.triagem DROP CONSTRAINT IF EXISTS triagem_enfnumfunc_fkey;
ALTER TABLE IF EXISTS ONLY public.prescricao DROP CONSTRAINT IF EXISTS prescricao_numepis_fkey;
ALTER TABLE IF EXISTS ONLY public.prescricao DROP CONSTRAINT IF EXISTS prescricao_mednumfunc_fkey;
ALTER TABLE IF EXISTS ONLY public.medico DROP CONSTRAINT IF EXISTS medico_mednumfunc_fkey;
ALTER TABLE IF EXISTS ONLY public.internamento DROP CONSTRAINT IF EXISTS internamento_numepis_fkey;
ALTER TABLE IF EXISTS ONLY public.funcionario DROP CONSTRAINT IF EXISTS funcionario_nomehosp_fkey;
ALTER TABLE IF EXISTS ONLY public.funcionario DROP CONSTRAINT IF EXISTS funcionario_idutilizador_fkey;
ALTER TABLE IF EXISTS ONLY public.episodio DROP CONSTRAINT IF EXISTS episodio_numutente_fkey;
ALTER TABLE IF EXISTS ONLY public.episodio DROP CONSTRAINT IF EXISTS episodio_nomehosp_fkey;
ALTER TABLE IF EXISTS ONLY public.enfermeiro DROP CONSTRAINT IF EXISTS enfermeiro_enfnumfunc_fkey;
ALTER TABLE IF EXISTS ONLY public.ato DROP CONSTRAINT IF EXISTS ato_numepis_fkey;
ALTER TABLE IF EXISTS ONLY public.ato DROP CONSTRAINT IF EXISTS ato_mednumfunc_fkey;
ALTER TABLE IF EXISTS ONLY public.ato DROP CONSTRAINT IF EXISTS ato_idtipoato_fkey;
ALTER TABLE IF EXISTS ONLY public.utilizador DROP CONSTRAINT IF EXISTS utilizador_username_key;
ALTER TABLE IF EXISTS ONLY public.utilizador DROP CONSTRAINT IF EXISTS utilizador_pkey;
ALTER TABLE IF EXISTS ONLY public.triagem DROP CONSTRAINT IF EXISTS triagem_pkey;
ALTER TABLE IF EXISTS ONLY public.tipoato DROP CONSTRAINT IF EXISTS tipoato_pkey;
ALTER TABLE IF EXISTS ONLY public.tipoato DROP CONSTRAINT IF EXISTS tipoato_designacao_key;
ALTER TABLE IF EXISTS ONLY public.t1_utente DROP CONSTRAINT IF EXISTS t1_utente_pkey;
ALTER TABLE IF EXISTS ONLY public.prescricao DROP CONSTRAINT IF EXISTS prescricao_pkey;
ALTER TABLE IF EXISTS ONLY public.medico DROP CONSTRAINT IF EXISTS medico_pkey;
ALTER TABLE IF EXISTS ONLY public.internamento DROP CONSTRAINT IF EXISTS internamento_pkey;
ALTER TABLE IF EXISTS ONLY public.hospital DROP CONSTRAINT IF EXISTS hospital_pkey;
ALTER TABLE IF EXISTS ONLY public.funcionario DROP CONSTRAINT IF EXISTS funcionario_pkey;
ALTER TABLE IF EXISTS ONLY public.episodio DROP CONSTRAINT IF EXISTS episodio_pkey;
ALTER TABLE IF EXISTS ONLY public.enfermeiro DROP CONSTRAINT IF EXISTS enfermeiro_pkey;
ALTER TABLE IF EXISTS ONLY public.ato DROP CONSTRAINT IF EXISTS ato_pkey;
ALTER TABLE IF EXISTS public.utilizador ALTER COLUMN idutilizador DROP DEFAULT;
ALTER TABLE IF EXISTS public.tipoato ALTER COLUMN idtipoato DROP DEFAULT;
ALTER TABLE IF EXISTS public.t1_utente ALTER COLUMN numutente DROP DEFAULT;
ALTER TABLE IF EXISTS public.prescricao ALTER COLUMN idprescricao DROP DEFAULT;
ALTER TABLE IF EXISTS public.funcionario ALTER COLUMN idfuncionario DROP DEFAULT;
ALTER TABLE IF EXISTS public.episodio ALTER COLUMN numepis DROP DEFAULT;
ALTER TABLE IF EXISTS public.ato ALTER COLUMN idato DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.utilizador_idutilizador_seq;
DROP TABLE IF EXISTS public.utilizador;
DROP TABLE IF EXISTS public.triagem;
DROP SEQUENCE IF EXISTS public.tipoato_idtipoato_seq;
DROP TABLE IF EXISTS public.tipoato;
DROP SEQUENCE IF EXISTS public.t1_utente_numutente_seq;
DROP TABLE IF EXISTS public.t1_utente;
DROP SEQUENCE IF EXISTS public.prescricao_idprescricao_seq;
DROP TABLE IF EXISTS public.prescricao;
DROP TABLE IF EXISTS public.medico;
DROP TABLE IF EXISTS public.internamento;
DROP TABLE IF EXISTS public.hospital;
DROP SEQUENCE IF EXISTS public.funcionario_idfuncionario_seq;
DROP TABLE IF EXISTS public.funcionario;
DROP SEQUENCE IF EXISTS public.episodio_numepis_seq;
DROP TABLE IF EXISTS public.episodio;
DROP TABLE IF EXISTS public.enfermeiro;
DROP SEQUENCE IF EXISTS public.ato_idato_seq;
DROP TABLE IF EXISTS public.ato;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ato; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ato (
    idato integer NOT NULL,
    numepis integer,
    mednumfunc integer,
    idtipoato integer,
    datahorainic timestamp without time zone,
    datahorafim timestamp without time zone
);


--
-- Name: ato_idato_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ato_idato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ato_idato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ato_idato_seq OWNED BY public.ato.idato;


--
-- Name: enfermeiro; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enfermeiro (
    enfnumfunc integer NOT NULL,
    grau character varying
);


--
-- Name: episodio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.episodio (
    numepis integer NOT NULL,
    nomehosp character varying,
    numutente integer,
    idestadoatual integer,
    datahorainicio timestamp without time zone,
    datahorasaida timestamp without time zone
);


--
-- Name: episodio_numepis_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.episodio_numepis_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: episodio_numepis_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.episodio_numepis_seq OWNED BY public.episodio.numepis;


--
-- Name: funcionario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.funcionario (
    idfuncionario integer NOT NULL,
    nome character varying,
    apelido character varying,
    sexo character varying,
    nomehosp character varying,
    idutilizador integer
);


--
-- Name: funcionario_idfuncionario_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.funcionario_idfuncionario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: funcionario_idfuncionario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.funcionario_idfuncionario_seq OWNED BY public.funcionario.idfuncionario;


--
-- Name: hospital; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hospital (
    nomehosp character varying NOT NULL,
    localizacao character varying
);


--
-- Name: internamento; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.internamento (
    numepis integer NOT NULL,
    cama_quarto character varying,
    servico character varying,
    datahorainicio timestamp without time zone
);


--
-- Name: medico; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medico (
    mednumfunc integer NOT NULL,
    especialidade character varying,
    estagiario boolean
);


--
-- Name: prescricao; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prescricao (
    idprescricao integer NOT NULL,
    numepis integer,
    mednumfunc integer,
    medicamento character varying,
    dosagem character varying,
    frequencia character varying,
    duracao character varying,
    datahoraprescricao timestamp without time zone
);


--
-- Name: prescricao_idprescricao_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prescricao_idprescricao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prescricao_idprescricao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prescricao_idprescricao_seq OWNED BY public.prescricao.idprescricao;


--
-- Name: t1_utente; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t1_utente (
    numutente integer NOT NULL,
    nome character varying,
    apelido character varying,
    localidade character varying,
    sexo character varying,
    datanasc date
);


--
-- Name: t1_utente_numutente_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t1_utente_numutente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t1_utente_numutente_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t1_utente_numutente_seq OWNED BY public.t1_utente.numutente;


--
-- Name: tipoato; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tipoato (
    idtipoato integer NOT NULL,
    designacao character varying
);


--
-- Name: tipoato_idtipoato_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tipoato_idtipoato_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tipoato_idtipoato_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tipoato_idtipoato_seq OWNED BY public.tipoato.idtipoato;


--
-- Name: triagem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.triagem (
    numepis integer NOT NULL,
    enfnumfunc integer,
    idprioridade_cor integer,
    sintomas character varying,
    tensaoarterial character varying,
    temperatura double precision
);


--
-- Name: utilizador; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.utilizador (
    idutilizador integer NOT NULL,
    username character varying,
    passwordhash character varying,
    idperfil integer
);


--
-- Name: utilizador_idutilizador_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.utilizador_idutilizador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: utilizador_idutilizador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.utilizador_idutilizador_seq OWNED BY public.utilizador.idutilizador;


--
-- Name: ato idato; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ato ALTER COLUMN idato SET DEFAULT nextval('public.ato_idato_seq'::regclass);


--
-- Name: episodio numepis; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.episodio ALTER COLUMN numepis SET DEFAULT nextval('public.episodio_numepis_seq'::regclass);


--
-- Name: funcionario idfuncionario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionario ALTER COLUMN idfuncionario SET DEFAULT nextval('public.funcionario_idfuncionario_seq'::regclass);


--
-- Name: prescricao idprescricao; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescricao ALTER COLUMN idprescricao SET DEFAULT nextval('public.prescricao_idprescricao_seq'::regclass);


--
-- Name: t1_utente numutente; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t1_utente ALTER COLUMN numutente SET DEFAULT nextval('public.t1_utente_numutente_seq'::regclass);


--
-- Name: tipoato idtipoato; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipoato ALTER COLUMN idtipoato SET DEFAULT nextval('public.tipoato_idtipoato_seq'::regclass);


--
-- Name: utilizador idutilizador; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.utilizador ALTER COLUMN idutilizador SET DEFAULT nextval('public.utilizador_idutilizador_seq'::regclass);


--
-- Data for Name: ato; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ato (idato, numepis, mednumfunc, idtipoato, datahorainic, datahorafim) FROM stdin;
1	1	2	1	2026-05-19 14:57:19	\N
2	85	2	2	2026-05-24 11:04:01.904432	2026-05-24 12:46:01.904432
3	87	2	3	2026-05-13 18:15:01.929784	2026-05-13 19:36:01.929784
4	88	2	1	2026-05-24 12:16:01.931053	2026-05-24 14:10:01.931053
5	91	2	4	2026-05-25 16:21:01.943551	2026-05-25 17:51:01.943551
6	92	2	1	2026-05-15 21:18:01.945435	2026-05-15 22:42:01.945435
7	93	2	2	2026-05-03 10:14:01.948504	2026-05-03 11:50:01.948504
8	97	2	3	2026-04-29 21:17:01.961095	2026-04-29 23:06:01.961095
9	98	2	2	2026-05-20 17:36:01.964393	2026-05-20 18:50:01.964393
10	99	2	3	2026-05-12 08:48:01.968738	2026-05-12 11:03:01.968738
11	100	2	2	2026-05-17 09:41:01.972684	2026-05-17 11:34:01.972684
12	102	2	4	2026-05-16 14:31:01.979199	2026-05-16 15:32:01.979199
13	103	2	4	2026-05-06 23:39:01.980243	2026-05-07 01:08:01.980243
14	104	2	4	2026-05-06 23:22:01.983045	2026-05-07 01:04:01.983045
15	105	2	3	2026-05-01 12:17:01.992845	2026-05-01 12:39:01.992845
16	106	2	3	2026-05-18 12:43:02.003011	2026-05-18 14:18:02.003011
17	112	2	1	2026-05-14 11:15:02.019475	2026-05-14 13:24:02.019475
18	113	2	1	2026-05-04 15:53:02.024117	2026-05-04 17:42:02.024117
19	115	2	2	2026-05-27 17:10:02.030577	2026-05-27 18:29:02.030577
20	119	2	4	2026-05-17 14:08:02.039819	2026-05-17 15:02:02.039819
21	121	2	1	2026-05-10 20:46:02.046655	2026-05-10 22:08:02.046655
22	122	2	4	2026-05-07 22:39:02.04767	2026-05-07 23:53:02.04767
23	125	2	4	2026-04-29 13:03:02.060097	2026-04-29 13:11:02.060097
24	126	2	4	2026-05-25 12:34:02.065719	2026-05-25 14:19:02.065719
25	127	2	4	2026-05-11 08:51:02.071607	2026-05-11 10:21:02.071607
26	128	2	1	2026-05-18 10:21:02.075746	2026-05-18 11:55:02.075746
27	129	2	4	2026-05-08 12:56:02.081382	2026-05-08 13:37:02.081382
28	130	2	2	2026-05-27 16:24:02.084131	2026-05-27 17:57:02.084131
29	132	2	2	2026-04-30 12:48:02.092758	2026-04-30 14:14:02.092758
30	133	2	2	2026-05-24 12:53:02.09374	2026-05-24 13:59:02.09374
31	134	2	4	2026-05-11 17:55:02.097886	2026-05-11 18:43:02.097886
32	136	2	4	2026-05-07 21:23:02.107313	2026-05-07 23:09:02.107313
33	137	2	1	2026-05-20 11:22:02.110255	2026-05-20 12:48:02.110255
34	138	2	2	2026-05-05 18:58:02.113767	2026-05-05 19:56:02.113767
35	140	2	4	2026-05-02 11:31:02.12067	2026-05-02 13:40:02.12067
36	144	2	4	2026-04-30 16:38:02.127959	2026-04-30 17:02:02.127959
37	147	2	1	2026-05-14 17:05:12.437059	2026-05-14 17:47:12.437059
38	148	2	4	2026-05-28 08:33:12.438316	2026-05-28 10:54:12.438316
39	149	2	4	2026-05-29 12:06:12.45265	2026-05-29 13:44:12.45265
40	150	2	4	2026-05-26 22:01:12.455327	2026-05-26 22:53:12.455327
41	151	2	2	2026-05-26 18:24:12.457688	2026-05-26 20:14:12.457688
42	152	2	2	2026-05-05 19:10:12.460653	2026-05-05 20:40:12.460653
43	153	2	2	2026-05-14 18:26:12.463615	2026-05-14 19:11:12.463615
44	154	2	1	2026-05-06 17:07:12.466875	2026-05-06 18:55:12.466875
45	155	2	3	2026-05-06 12:47:12.469922	2026-05-06 13:49:12.469922
46	156	2	1	2026-05-04 18:52:12.473307	2026-05-04 20:16:12.473307
47	158	2	2	2026-05-14 20:28:12.480921	2026-05-14 21:08:12.480921
48	159	2	1	2026-05-21 09:07:12.481832	2026-05-21 11:00:12.481832
49	160	2	3	2026-05-28 16:49:12.48478	2026-05-28 17:28:12.48478
50	161	2	2	2026-05-22 12:41:12.487272	2026-05-22 14:19:12.487272
51	162	2	2	2026-05-28 14:14:12.489759	2026-05-28 15:13:12.489759
52	163	2	3	2026-05-12 13:32:12.492135	2026-05-12 14:08:12.492135
53	164	2	3	2026-05-21 11:42:12.494947	2026-05-21 13:13:12.494947
54	165	2	1	2026-05-29 21:38:12.503172	2026-05-29 21:52:12.503172
55	167	2	2	2026-05-18 09:33:12.52161	2026-05-18 10:45:12.52161
56	168	2	4	2026-05-29 11:26:12.523963	2026-05-29 12:30:12.523963
57	170	2	3	2026-05-22 20:00:12.532089	2026-05-22 21:24:12.532089
58	171	2	3	2026-05-31 22:54:12.535965	2026-05-31 23:02:12.535965
59	176	2	1	2026-05-07 10:47:12.547406	2026-05-07 12:47:12.547406
60	179	2	2	2026-05-08 15:16:12.553378	2026-05-08 17:10:12.553378
61	185	2	3	2026-05-04 21:36:12.565273	2026-05-04 22:49:12.565273
62	186	2	1	2026-05-07 21:06:12.572525	2026-05-07 22:12:12.572525
63	188	2	2	2026-05-31 23:48:12.581328	2026-06-01 01:23:12.581328
64	189	2	2	2026-05-12 12:36:12.584013	2026-05-12 13:43:12.584013
65	190	2	1	2026-05-17 19:31:12.589321	2026-05-17 20:49:12.589321
66	193	2	2	2026-05-23 15:36:12.597479	2026-05-23 17:49:12.597479
67	196	2	2	2026-05-07 22:54:12.604498	2026-05-08 00:25:12.604498
68	199	2	1	2026-05-22 08:58:12.611008	2026-05-22 09:04:12.611008
69	202	2	3	2026-05-28 23:48:12.614781	2026-05-29 00:21:12.614781
70	203	2	4	2026-05-21 16:41:12.616815	2026-05-21 18:03:12.616815
71	204	2	1	2026-05-05 11:02:12.621884	2026-05-05 11:45:12.621884
\.


--
-- Data for Name: enfermeiro; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enfermeiro (enfnumfunc, grau) FROM stdin;
1	Especialista
\.


--
-- Data for Name: episodio; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.episodio (numepis, nomehosp, numutente, idestadoatual, datahorainicio, datahorasaida) FROM stdin;
2	Hospital PRODIGI Central	100001	1	2026-05-19 13:47:09.578015	\N
3	Hospital PRODIGI Central	100001	1	2026-05-19 14:11:29.035392	\N
4	Hospital PRODIGI Central	100001	1	2026-05-19 14:26:33.270095	\N
88	Hospital PRODIGI Central	0	5	2026-05-24 11:46:01.931053	2026-05-24 18:46:01.931053
1	Hospital PRODIGI Central	100001	5	2026-05-19 13:08:39.46061	2026-05-19 14:49:23.201732
5	Hospital PRODIGI Central	100001	5	2026-05-04 16:54:05.313764	2026-05-04 17:49:05.313764
6	Hospital PRODIGI Central	100002	5	2026-04-01 13:44:05.323502	2026-04-01 14:56:05.323502
7	Hospital PRODIGI Central	100003	5	2026-04-30 14:41:05.326795	2026-04-30 15:22:05.326795
8	Hospital PRODIGI Central	100002	5	2026-05-16 21:14:05.327984	2026-05-16 22:18:05.327984
9	Hospital PRODIGI Central	100002	5	2026-04-05 04:40:05.329011	2026-04-05 06:31:05.329011
10	Hospital PRODIGI Central	100001	5	2026-04-03 02:11:05.330166	2026-04-03 02:16:05.330166
11	Hospital PRODIGI Central	100003	5	2026-05-10 09:17:05.331803	2026-05-10 11:49:05.331803
12	Hospital PRODIGI Central	100001	5	2026-04-27 02:42:05.333831	2026-04-27 04:02:05.333831
13	Hospital PRODIGI Central	100002	5	2026-04-14 21:06:05.335529	2026-04-14 23:33:05.335529
14	Hospital PRODIGI Central	100001	5	2026-04-24 01:13:05.336543	2026-04-24 03:05:05.336543
15	Hospital PRODIGI Central	100003	5	2026-04-06 16:26:05.337463	2026-04-06 17:28:05.337463
16	Hospital PRODIGI Central	100002	5	2026-05-12 15:39:05.338565	2026-05-12 16:48:05.338565
17	Hospital PRODIGI Central	100003	5	2026-04-12 00:00:05.339485	2026-04-12 00:19:05.339485
18	Hospital PRODIGI Central	100002	5	2026-04-06 04:49:05.340398	2026-04-06 05:57:05.340398
19	Hospital PRODIGI Central	100001	5	2026-05-09 04:48:05.341298	2026-05-09 05:09:05.341298
20	Hospital PRODIGI Central	100002	5	2026-04-29 11:36:05.342333	2026-04-29 12:04:05.342333
21	Hospital PRODIGI Central	100003	5	2026-05-16 00:11:05.343238	2026-05-16 00:55:05.343238
22	Hospital PRODIGI Central	100001	5	2026-04-20 09:43:05.344148	2026-04-20 10:29:05.344148
23	Hospital PRODIGI Central	100002	5	2026-03-30 15:37:05.345031	2026-03-30 16:50:05.345031
24	Hospital PRODIGI Central	100001	5	2026-05-11 18:18:05.346047	2026-05-11 19:27:05.346047
25	Hospital PRODIGI Central	100003	5	2026-03-25 06:12:05.350956	2026-03-25 06:53:05.350956
26	Hospital PRODIGI Central	100001	5	2026-05-14 14:16:05.355998	2026-05-14 15:19:05.355998
27	Hospital PRODIGI Central	100002	5	2026-05-19 19:19:05.357453	2026-05-19 19:35:05.357453
28	Hospital PRODIGI Central	100003	5	2026-04-04 22:36:05.358939	2026-04-04 23:49:05.358939
29	Hospital PRODIGI Central	100002	5	2026-04-02 17:29:05.359866	2026-04-02 18:46:05.359866
30	Hospital PRODIGI Central	100002	5	2026-04-13 23:27:05.360866	2026-04-14 00:45:05.360866
31	Hospital PRODIGI Central	100003	5	2026-03-24 14:24:05.361975	2026-03-24 16:04:05.361975
32	Hospital PRODIGI Central	100003	5	2026-04-23 06:04:05.362919	2026-04-23 06:42:05.362919
33	Hospital PRODIGI Central	100003	5	2026-04-29 08:45:05.363865	2026-04-29 11:22:05.363865
34	Hospital PRODIGI Central	100001	5	2026-03-30 05:31:05.365421	2026-03-30 05:36:05.365421
35	Hospital PRODIGI Central	100002	5	2026-04-25 17:23:05.366796	2026-04-25 18:37:05.366796
36	Hospital PRODIGI Central	100002	5	2026-05-16 20:32:05.368047	2026-05-16 21:52:05.368047
37	Hospital PRODIGI Central	100002	5	2026-04-22 15:03:05.369197	2026-04-22 17:35:05.369197
38	Hospital PRODIGI Central	100002	5	2026-05-15 08:23:05.371037	2026-05-15 09:46:05.371037
39	Hospital PRODIGI Central	100003	5	2026-04-19 10:02:05.372933	2026-04-19 10:43:05.372933
40	Hospital PRODIGI Central	100002	5	2026-05-06 17:55:05.374929	2026-05-06 19:15:05.374929
41	Hospital PRODIGI Central	100001	5	2026-05-02 17:23:05.375948	2026-05-02 18:10:05.375948
42	Hospital PRODIGI Central	100003	5	2026-05-11 23:23:05.376906	2026-05-11 23:57:05.376906
43	Hospital PRODIGI Central	100003	5	2026-05-01 16:17:05.377824	2026-05-01 17:10:05.377824
44	Hospital PRODIGI Central	100001	5	2026-04-08 21:48:05.378807	2026-04-09 00:27:05.378807
45	Hospital PRODIGI Central	100001	5	2026-03-28 06:26:05.383056	2026-03-28 08:36:05.383056
46	Hospital PRODIGI Central	100001	5	2026-05-06 11:56:05.387373	2026-05-06 13:04:05.387373
47	Hospital PRODIGI Central	100001	5	2026-05-13 18:13:05.388299	2026-05-13 19:08:05.388299
48	Hospital PRODIGI Central	100002	5	2026-03-25 13:25:05.389251	2026-03-25 15:49:05.389251
49	Hospital PRODIGI Central	100001	5	2026-04-14 15:29:05.390748	2026-04-14 16:54:05.390748
50	Hospital PRODIGI Central	100002	5	2026-04-19 09:42:05.391622	2026-04-19 10:38:05.391622
51	Hospital PRODIGI Central	100002	5	2026-04-03 09:12:05.392511	2026-04-03 11:49:05.392511
52	Hospital PRODIGI Central	100001	5	2026-03-30 20:51:05.3934	2026-03-30 22:05:05.3934
53	Hospital PRODIGI Central	100001	5	2026-05-10 20:32:05.394401	2026-05-10 21:22:05.394401
54	Hospital PRODIGI Central	100001	5	2026-04-29 14:10:05.395304	2026-04-29 16:45:05.395304
55	Hospital PRODIGI Central	100003	5	2026-04-13 08:58:05.39619	2026-04-13 09:54:05.39619
56	Hospital PRODIGI Central	100003	5	2026-04-04 09:37:05.397853	2026-04-04 11:03:05.397853
57	Hospital PRODIGI Central	100003	5	2026-05-19 13:03:05.399497	2026-05-19 14:21:05.399497
58	Hospital PRODIGI Central	100001	5	2026-04-23 22:51:05.400742	2026-04-23 23:32:05.400742
59	Hospital PRODIGI Central	100001	5	2026-05-22 05:43:05.402035	2026-05-22 07:07:05.402035
60	Hospital PRODIGI Central	100003	5	2026-05-09 21:45:05.403755	2026-05-09 22:20:05.403755
61	Hospital PRODIGI Central	100003	5	2026-04-02 02:35:05.405218	2026-04-02 03:38:05.405218
62	Hospital PRODIGI Central	100003	5	2026-05-09 06:26:05.406833	2026-05-09 07:25:05.406833
63	Hospital PRODIGI Central	100003	5	2026-05-06 14:20:05.407839	2026-05-06 16:00:05.407839
64	Hospital PRODIGI Central	100002	5	2026-05-18 11:03:05.408804	2026-05-18 12:46:05.408804
65	Hospital PRODIGI Central	100001	5	2026-05-21 05:45:05.413565	2026-05-21 05:58:05.413565
66	Hospital PRODIGI Central	100003	5	2026-04-07 05:15:05.417867	2026-04-07 07:21:05.417867
67	Hospital PRODIGI Central	100002	5	2026-05-08 03:01:05.419893	2026-05-08 05:04:05.419893
68	Hospital PRODIGI Central	100001	5	2026-04-06 10:32:05.421356	2026-04-06 13:16:05.421356
69	Hospital PRODIGI Central	100002	5	2026-05-10 20:18:05.422313	2026-05-10 22:54:05.422313
70	Hospital PRODIGI Central	100001	5	2026-04-05 21:52:05.423205	2026-04-05 23:24:05.423205
71	Hospital PRODIGI Central	100002	5	2026-04-08 21:00:05.424131	2026-04-08 22:30:05.424131
72	Hospital PRODIGI Central	100001	5	2026-05-09 19:29:05.425027	2026-05-09 19:52:05.425027
73	Hospital PRODIGI Central	100003	5	2026-03-31 18:58:05.426845	2026-03-31 19:05:05.426845
74	Hospital PRODIGI Central	100002	5	2026-04-28 18:17:05.428811	2026-04-28 18:44:05.428811
75	Hospital PRODIGI Central	100003	5	2026-03-31 13:50:05.430136	2026-03-31 14:29:05.430136
76	Hospital PRODIGI Central	100001	5	2026-05-14 22:30:05.431313	2026-05-14 23:27:05.431313
77	Hospital PRODIGI Central	100003	5	2026-05-07 10:20:05.432507	2026-05-07 11:25:05.432507
78	Hospital PRODIGI Central	100003	5	2026-04-14 12:05:05.434018	2026-04-14 14:23:05.434018
79	Hospital PRODIGI Central	100001	5	2026-05-02 20:51:05.435543	2026-05-02 21:41:05.435543
80	Hospital PRODIGI Central	100003	5	2026-04-25 06:08:05.437	2026-04-25 06:45:05.437
81	Hospital PRODIGI Central	100001	5	2026-05-13 18:55:05.438214	2026-05-13 19:34:05.438214
82	Hospital PRODIGI Central	100001	5	2026-03-26 00:40:05.439138	2026-03-26 01:14:05.439138
83	Hospital PRODIGI Central	100002	5	2026-04-19 13:29:05.440038	2026-04-19 14:40:05.440038
84	Hospital PRODIGI Central	100001	5	2026-03-25 17:53:05.440935	2026-03-25 18:39:05.440935
85	Hospital PRODIGI Central	100007	3	2026-05-24 10:18:01.904432	\N
86	Hospital PRODIGI Central	100003	1	2026-05-27 15:52:01.913064	\N
87	Hospital PRODIGI Central	100007	5	2026-05-13 17:22:01.929784	2026-05-14 01:22:01.929784
89	Hospital PRODIGI Central	100002	1	2026-04-30 15:11:01.938832	\N
90	Hospital PRODIGI Central	100002	2	2026-05-28 11:21:01.942476	\N
91	Hospital PRODIGI Central	0	3	2026-05-25 15:45:01.943551	\N
92	Hospital PRODIGI Central	100006	3	2026-05-15 20:33:01.945435	\N
93	Hospital PRODIGI Central	100004	3	2026-05-03 09:42:01.948504	\N
94	Hospital PRODIGI Central	100002	2	2026-05-01 12:57:01.951593	\N
95	Hospital PRODIGI Central	0	2	2026-05-01 13:30:01.957764	\N
96	Hospital PRODIGI Central	10223	2	2026-05-28 19:46:01.959534	\N
97	Hospital PRODIGI Central	100005	4	2026-04-29 20:26:01.961095	\N
98	Hospital PRODIGI Central	100002	5	2026-05-20 16:55:01.964393	2026-05-20 22:55:01.964393
99	Hospital PRODIGI Central	100005	5	2026-05-12 08:09:01.968738	2026-05-12 11:09:01.968738
100	Hospital PRODIGI Central	0	5	2026-05-17 08:43:01.972684	2026-05-17 09:43:01.972684
101	Hospital PRODIGI Central	100008	1	2026-04-28 14:57:01.976035	\N
102	Hospital PRODIGI Central	100003	3	2026-05-16 13:13:01.979199	\N
103	Hospital PRODIGI Central	100006	4	2026-05-06 22:14:01.980243	\N
104	Hospital PRODIGI Central	100006	4	2026-05-06 22:27:01.983045	\N
105	Hospital PRODIGI Central	100002	4	2026-05-01 10:59:01.992845	\N
106	Hospital PRODIGI Central	100004	3	2026-05-18 11:18:02.003011	\N
107	Hospital PRODIGI Central	100004	1	2026-05-07 20:22:02.009567	\N
108	Hospital PRODIGI Central	0	2	2026-05-09 15:21:02.012583	\N
109	Hospital PRODIGI Central	100007	2	2026-05-10 18:13:02.014682	\N
110	Hospital PRODIGI Central	100002	1	2026-05-26 19:03:02.01719	\N
111	Hospital PRODIGI Central	100002	1	2026-05-25 20:45:02.018642	\N
112	Hospital PRODIGI Central	100003	3	2026-05-14 10:26:02.019475	\N
113	Hospital PRODIGI Central	100007	4	2026-05-04 15:06:02.024117	\N
114	Hospital PRODIGI Central	100003	1	2026-05-11 11:00:02.027408	\N
115	Hospital PRODIGI Central	100004	5	2026-05-27 15:41:02.030577	2026-05-27 22:41:02.030577
116	Hospital PRODIGI Central	100002	2	2026-05-12 15:01:02.032432	\N
117	Hospital PRODIGI Central	100007	2	2026-05-17 14:54:02.035801	\N
118	Hospital PRODIGI Central	100004	2	2026-05-21 22:23:02.038014	\N
119	Hospital PRODIGI Central	100008	4	2026-05-17 12:39:02.039819	\N
120	Hospital PRODIGI Central	100002	1	2026-05-25 11:33:02.043367	\N
121	Hospital PRODIGI Central	100004	5	2026-05-10 19:23:02.046655	2026-05-10 22:23:02.046655
122	Hospital PRODIGI Central	100002	3	2026-05-07 22:06:02.04767	\N
123	Hospital PRODIGI Central	100005	1	2026-05-01 20:56:02.050947	\N
124	Hospital PRODIGI Central	10223	2	2026-05-27 18:57:02.054905	\N
125	Hospital PRODIGI Central	10223	3	2026-04-29 11:41:02.060097	\N
126	Hospital PRODIGI Central	100003	3	2026-05-25 11:53:02.065719	\N
127	Hospital PRODIGI Central	100002	4	2026-05-11 07:48:02.071607	\N
128	Hospital PRODIGI Central	100006	3	2026-05-18 09:27:02.075746	\N
129	Hospital PRODIGI Central	100002	4	2026-05-08 12:04:02.081382	\N
130	Hospital PRODIGI Central	100007	3	2026-05-27 15:01:02.084131	\N
131	Hospital PRODIGI Central	100005	1	2026-05-26 10:09:02.089305	\N
132	Hospital PRODIGI Central	100003	4	2026-04-30 11:18:02.092758	\N
133	Hospital PRODIGI Central	100004	3	2026-05-24 12:10:02.09374	\N
134	Hospital PRODIGI Central	0	5	2026-05-11 16:55:02.097886	2026-05-12 00:55:02.097886
135	Hospital PRODIGI Central	100003	2	2026-05-06 20:35:02.101893	\N
136	Hospital PRODIGI Central	100001	3	2026-05-07 20:32:02.107313	\N
137	Hospital PRODIGI Central	100006	3	2026-05-20 10:02:02.110255	\N
138	Hospital PRODIGI Central	0	5	2026-05-05 17:40:02.113767	2026-05-05 18:40:02.113767
139	Hospital PRODIGI Central	100006	2	2026-05-02 07:52:02.11722	\N
140	Hospital PRODIGI Central	100005	5	2026-05-02 10:57:02.12067	2026-05-02 15:57:02.12067
141	Hospital PRODIGI Central	100007	2	2026-05-16 16:08:02.122337	\N
142	Hospital PRODIGI Central	100007	2	2026-05-15 17:21:02.125021	\N
143	Hospital PRODIGI Central	100008	2	2026-05-06 13:10:02.126137	\N
144	Hospital PRODIGI Central	100004	4	2026-04-30 15:08:02.127959	\N
145	Hospital PRODIGI Central	100003	2	2026-05-11 07:27:12.422827	\N
146	Hospital PRODIGI Central	10223	1	2026-05-31 17:00:12.431294	\N
147	Hospital PRODIGI Central	100005	5	2026-05-14 16:03:12.437059	2026-05-14 21:03:12.437059
148	Hospital PRODIGI Central	100006	3	2026-05-28 07:54:12.438316	\N
149	Hospital PRODIGI Central	100003	3	2026-05-29 11:30:12.45265	\N
150	Hospital PRODIGI Central	100001	3	2026-05-26 20:58:12.455327	\N
151	Hospital PRODIGI Central	100002	5	2026-05-26 17:27:12.457688	2026-05-26 18:27:12.457688
152	Hospital PRODIGI Central	100005	4	2026-05-05 17:58:12.460653	\N
153	Hospital PRODIGI Central	10223	3	2026-05-14 17:11:12.463615	\N
154	Hospital PRODIGI Central	100002	3	2026-05-06 16:17:12.466875	\N
155	Hospital PRODIGI Central	100006	4	2026-05-06 11:18:12.469922	\N
156	Hospital PRODIGI Central	100004	4	2026-05-04 18:07:12.473307	\N
157	Hospital PRODIGI Central	100007	1	2026-05-14 13:39:12.476958	\N
158	Hospital PRODIGI Central	100002	4	2026-05-14 19:06:12.480921	\N
159	Hospital PRODIGI Central	100001	4	2026-05-21 08:28:12.481832	\N
160	Hospital PRODIGI Central	0	3	2026-05-28 15:56:12.48478	\N
161	Hospital PRODIGI Central	100004	3	2026-05-22 11:50:12.487272	\N
162	Hospital PRODIGI Central	100008	5	2026-05-28 13:01:12.489759	2026-05-28 15:01:12.489759
163	Hospital PRODIGI Central	100001	3	2026-05-12 12:28:12.492135	\N
164	Hospital PRODIGI Central	100006	3	2026-05-21 10:50:12.494947	\N
165	Hospital PRODIGI Central	10223	3	2026-05-29 20:09:12.503172	\N
166	Hospital PRODIGI Central	100003	1	2026-05-23 14:24:12.51567	\N
167	Hospital PRODIGI Central	100006	5	2026-05-18 08:03:12.52161	2026-05-18 15:03:12.52161
168	Hospital PRODIGI Central	0	5	2026-05-29 10:24:12.523963	2026-05-29 12:24:12.523963
169	Hospital PRODIGI Central	100005	2	2026-05-21 16:54:12.5281	\N
170	Hospital PRODIGI Central	100007	4	2026-05-22 18:57:12.532089	\N
171	Hospital PRODIGI Central	100008	5	2026-05-31 21:24:12.535965	2026-06-01 04:24:12.535965
172	Hospital PRODIGI Central	100004	1	2026-05-11 21:50:12.54084	\N
173	Hospital PRODIGI Central	0	1	2026-05-11 09:34:12.544956	\N
174	Hospital PRODIGI Central	0	2	2026-05-11 19:39:12.545686	\N
175	Hospital PRODIGI Central	10223	2	2026-05-09 10:07:12.546321	\N
176	Hospital PRODIGI Central	100004	4	2026-05-07 09:57:12.547406	\N
177	Hospital PRODIGI Central	100003	1	2026-05-28 17:48:12.548945	\N
178	Hospital PRODIGI Central	100002	1	2026-05-16 21:51:12.55188	\N
179	Hospital PRODIGI Central	10223	4	2026-05-08 14:37:12.553378	\N
180	Hospital PRODIGI Central	100006	2	2026-05-18 13:50:12.554207	\N
181	Hospital PRODIGI Central	100001	2	2026-05-21 16:57:12.556997	\N
182	Hospital PRODIGI Central	100006	2	2026-05-28 16:18:12.559142	\N
183	Hospital PRODIGI Central	100006	2	2026-05-17 19:59:12.560409	\N
184	Hospital PRODIGI Central	100004	1	2026-05-28 12:18:12.561564	\N
185	Hospital PRODIGI Central	100007	3	2026-05-04 21:02:12.565273	\N
186	Hospital PRODIGI Central	100001	3	2026-05-07 19:40:12.572525	\N
187	Hospital PRODIGI Central	0	2	2026-05-19 08:40:12.577844	\N
188	Hospital PRODIGI Central	10223	5	2026-05-31 22:42:12.581328	2026-06-01 06:42:12.581328
189	Hospital PRODIGI Central	100005	5	2026-05-12 11:25:12.584013	2026-05-12 14:25:12.584013
190	Hospital PRODIGI Central	10223	5	2026-05-17 18:52:12.589321	2026-05-17 22:52:12.589321
191	Hospital PRODIGI Central	100003	2	2026-05-05 15:51:12.592367	\N
192	Hospital PRODIGI Central	100008	2	2026-05-09 07:24:12.595505	\N
193	Hospital PRODIGI Central	100007	3	2026-05-23 15:06:12.597479	\N
194	Hospital PRODIGI Central	100005	2	2026-05-13 09:48:12.599212	\N
195	Hospital PRODIGI Central	100001	1	2026-05-28 15:13:12.603211	\N
196	Hospital PRODIGI Central	100005	5	2026-05-07 21:54:12.604498	2026-05-08 04:54:12.604498
197	Hospital PRODIGI Central	10223	2	2026-05-29 20:06:12.605366	\N
198	Hospital PRODIGI Central	100007	1	2026-05-06 09:15:12.609764	\N
199	Hospital PRODIGI Central	100005	3	2026-05-22 07:29:12.611008	\N
200	Hospital PRODIGI Central	100007	2	2026-05-13 09:37:12.61176	\N
201	Hospital PRODIGI Central	100001	2	2026-05-13 19:19:12.613731	\N
202	Hospital PRODIGI Central	100002	4	2026-05-28 22:38:12.614781	\N
203	Hospital PRODIGI Central	100006	3	2026-05-21 16:10:12.616815	\N
204	Hospital PRODIGI Central	100004	4	2026-05-05 09:48:12.621884	\N
\.


--
-- Data for Name: funcionario; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.funcionario (idfuncionario, nome, apelido, sexo, nomehosp, idutilizador) FROM stdin;
1	Ana	Santos	F	Hospital PRODIGI Central	2
2	Carlos	Silva	M	Hospital PRODIGI Central	1
\.


--
-- Data for Name: hospital; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hospital (nomehosp, localizacao) FROM stdin;
Hospital PRODIGI Central	Lisboa, Portugal
Hospital PRODIGI Norte	Porto, Portugal
\.


--
-- Data for Name: internamento; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.internamento (numepis, cama_quarto, servico, datahorainicio) FROM stdin;
1	301-A	Medicina Interna	2026-05-19 14:35:05.122713
87	4C	Cardiologia	2026-05-13 21:22:01.929784
88	4C	Ortopedia	2026-05-24 14:46:01.931053
97	1C	Cardiologia	2026-04-29 22:26:01.961095
98	4C	Cirurgia	2026-05-20 19:55:01.964393
99	3B	Ortopedia	2026-05-12 13:09:01.968738
100	5A	Ortopedia	2026-05-17 12:43:01.972684
103	2B	Medicina Interna	2026-05-07 00:14:01.980243
104	1A	Ortopedia	2026-05-07 03:27:01.983045
105	2B	Ortopedia	2026-05-01 14:59:01.992845
113	3C	Medicina Interna	2026-05-04 21:06:02.024117
115	4A	Ortopedia	2026-05-27 20:41:02.030577
119	5A	Ortopedia	2026-05-17 15:39:02.039819
121	3C	Medicina Interna	2026-05-11 00:23:02.046655
127	3B	Ortopedia	2026-05-11 13:48:02.071607
129	2C	Cardiologia	2026-05-08 15:04:02.081382
132	5C	Cardiologia	2026-04-30 14:18:02.092758
134	5C	Cirurgia	2026-05-11 18:55:02.097886
138	3A	Cardiologia	2026-05-05 21:40:02.113767
140	2A	Cardiologia	2026-05-02 13:57:02.12067
144	3C	Cirurgia	2026-04-30 17:08:02.127959
147	3A	Cirurgia	2026-05-14 19:03:12.437059
151	5B	Medicina Interna	2026-05-26 23:27:12.457688
152	4C	Medicina Interna	2026-05-05 19:58:12.460653
155	1B	Medicina Interna	2026-05-06 17:18:12.469922
156	4B	Medicina Interna	2026-05-04 22:07:12.473307
158	3C	Cardiologia	2026-05-14 23:06:12.480921
159	3A	Cirurgia	2026-05-21 11:28:12.481832
162	2A	Medicina Interna	2026-05-28 15:01:12.489759
167	1C	Cardiologia	2026-05-18 10:03:12.52161
168	5A	Ortopedia	2026-05-29 16:24:12.523963
170	4C	Ortopedia	2026-05-22 22:57:12.532089
171	3A	Medicina Interna	2026-05-31 23:24:12.535965
176	4C	Ortopedia	2026-05-07 15:57:12.547406
179	4C	Cardiologia	2026-05-08 17:37:12.553378
188	5A	Medicina Interna	2026-06-01 01:42:12.581328
189	5B	Ortopedia	2026-05-12 13:25:12.584013
190	1A	Medicina Interna	2026-05-17 23:52:12.589321
196	5B	Cirurgia	2026-05-08 02:54:12.604498
202	5C	Ortopedia	2026-05-29 03:38:12.614781
204	3B	Cirurgia	2026-05-05 11:48:12.621884
\.


--
-- Data for Name: medico; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.medico (mednumfunc, especialidade, estagiario) FROM stdin;
2	Medicina Interna	f
\.


--
-- Data for Name: prescricao; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.prescricao (idprescricao, numepis, mednumfunc, medicamento, dosagem, frequencia, duracao, datahoraprescricao) FROM stdin;
1	85	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:01.921794
2	87	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:01.936875
3	88	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:01.941087
4	91	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-05-28 15:27:01.947003
5	92	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:01.95003
6	93	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:01.95368
7	97	2	Omeprazol	20mg	1x/dia	30 dias	2026-05-28 15:27:01.966998
8	98	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:01.97125
9	99	2	Omeprazol	20mg	1x/dia	30 dias	2026-05-28 15:27:01.974672
10	100	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-05-28 15:27:01.978017
11	102	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:01.981669
12	103	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:01.985669
13	104	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:01.989094
14	105	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:02.007853
15	106	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:02.011265
16	112	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:02.025964
17	113	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:02.029246
18	115	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:02.034487
19	119	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:02.045355
20	121	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:02.049625
21	122	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-05-28 15:27:02.053719
22	125	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:02.069966
23	126	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:02.07434
24	127	2	Omeprazol	20mg	1x/dia	30 dias	2026-05-28 15:27:02.078937
25	128	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:02.082802
26	129	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-05-28 15:27:02.08708
27	130	2	Omeprazol	20mg	1x/dia	30 dias	2026-05-28 15:27:02.091574
28	132	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:02.096532
29	133	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:02.100337
30	134	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:02.105011
31	136	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-05-28 15:27:02.111817
32	137	2	Paracetamol	500mg	3x/dia	5 dias	2026-05-28 15:27:02.115808
33	138	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:02.11896
34	140	2	Metoclopramida	10mg	3x/dia	3 dias	2026-05-28 15:27:02.123995
35	144	2	Amoxicilina	875mg	2x/dia	10 dias	2026-05-28 15:27:02.130094
36	147	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.447825
37	148	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.453959
38	149	2	Amoxicilina	875mg	2x/dia	10 dias	2026-06-01 15:39:12.456583
39	150	2	Amoxicilina	875mg	2x/dia	10 dias	2026-06-01 15:39:12.45926
40	151	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.462307
41	152	2	Paracetamol	500mg	3x/dia	5 dias	2026-06-01 15:39:12.465668
42	153	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.46842
43	154	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.471626
44	155	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.475689
45	156	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.479163
46	158	2	Paracetamol	500mg	3x/dia	5 dias	2026-06-01 15:39:12.483345
47	159	2	Amoxicilina	875mg	2x/dia	10 dias	2026-06-01 15:39:12.486273
48	160	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.488574
49	161	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.490992
50	162	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.493741
51	163	2	Amoxicilina	875mg	2x/dia	10 dias	2026-06-01 15:39:12.496242
52	164	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.498437
53	165	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.520398
54	167	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.526143
55	168	2	Ibuprofeno	400mg	2x/dia	7 dias	2026-06-01 15:39:12.530681
56	170	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.539484
57	171	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.54371
58	176	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.55077
59	179	2	Paracetamol	500mg	3x/dia	5 dias	2026-06-01 15:39:12.55589
60	185	2	Amoxicilina	875mg	2x/dia	10 dias	2026-06-01 15:39:12.575789
61	186	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.580097
62	188	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.587043
63	189	2	Amoxicilina	875mg	2x/dia	10 dias	2026-06-01 15:39:12.591265
64	190	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.594557
65	193	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.601149
66	196	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.608292
67	199	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.612792
68	202	2	Omeprazol	20mg	1x/dia	30 dias	2026-06-01 15:39:12.619905
69	203	2	Metoclopramida	10mg	3x/dia	3 dias	2026-06-01 15:39:12.624506
70	204	2	Amoxicilina	875mg	2x/dia	10 dias	2026-06-01 15:39:12.627358
\.


--
-- Data for Name: t1_utente; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.t1_utente (numutente, nome, apelido, localidade, sexo, datanasc) FROM stdin;
100001	João	Silva	Lisboa	M	1990-05-15
100002	Ana	Santos	Porto	F	1985-08-22
100003	Pedro	Costa	Coimbra	M	1998-12-01
0	string	string	string	string	2026-05-27
10223	Nuno	Hipolito	Lisboa	Masc	2025-05-27
100004	Maria	Ferreira	Braga	F	1972-03-08
100005	Rui	Oliveira	Faro	M	2005-11-20
100006	Carla	Rodrigues	Setúbal	F	1965-07-14
100007	Tiago	Alves	Aveiro	M	1993-09-30
100008	Sofia	Martins	Évora	F	1980-02-05
\.


--
-- Data for Name: tipoato; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tipoato (idtipoato, designacao) FROM stdin;
1	Consulta
2	Exame
3	Procedimento
4	Outro
\.


--
-- Data for Name: triagem; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.triagem (numepis, enfnumfunc, idprioridade_cor, sintomas, tensaoarterial, temperatura) FROM stdin;
1	1	3	Febre alta e tosse seca	120/80	38.5
5	1	2	Dados sintéticos para treino IA #1	106/87	37.6
6	1	4	Dados sintéticos para treino IA #2	138/86	38.1
7	1	3	Dados sintéticos para treino IA #3	111/74	37.5
8	1	2	Dados sintéticos para treino IA #4	124/62	37.5
9	1	5	Dados sintéticos para treino IA #5	134/61	38.8
10	1	1	Dados sintéticos para treino IA #6	117/85	37
11	1	5	Dados sintéticos para treino IA #7	125/63	36.4
12	1	4	Dados sintéticos para treino IA #8	107/78	36.5
13	1	5	Dados sintéticos para treino IA #9	109/90	37.8
14	1	5	Dados sintéticos para treino IA #10	135/87	38.7
15	1	3	Dados sintéticos para treino IA #11	139/81	37.1
16	1	3	Dados sintéticos para treino IA #12	122/73	39.5
17	1	3	Dados sintéticos para treino IA #13	109/63	36.1
18	1	4	Dados sintéticos para treino IA #14	119/61	38.3
19	1	3	Dados sintéticos para treino IA #15	136/65	36.5
20	1	1	Dados sintéticos para treino IA #16	107/67	38.5
21	1	3	Dados sintéticos para treino IA #17	121/75	36.9
22	1	3	Dados sintéticos para treino IA #18	102/85	37.8
23	1	4	Dados sintéticos para treino IA #19	107/64	36.3
24	1	4	Dados sintéticos para treino IA #20	139/64	36.9
25	1	3	Dados sintéticos para treino IA #21	107/69	36.7
26	1	4	Dados sintéticos para treino IA #22	133/83	38.3
27	1	3	Dados sintéticos para treino IA #23	125/65	37.5
28	1	4	Dados sintéticos para treino IA #24	101/67	37.7
29	1	4	Dados sintéticos para treino IA #25	130/82	39.4
30	1	4	Dados sintéticos para treino IA #26	137/67	36.3
31	1	4	Dados sintéticos para treino IA #27	129/81	37.7
32	1	2	Dados sintéticos para treino IA #28	125/72	36.4
33	1	5	Dados sintéticos para treino IA #29	121/69	38.9
34	1	1	Dados sintéticos para treino IA #30	121/82	38
35	1	4	Dados sintéticos para treino IA #31	128/82	37.4
36	1	4	Dados sintéticos para treino IA #32	136/82	39.3
37	1	5	Dados sintéticos para treino IA #33	138/79	36.3
38	1	4	Dados sintéticos para treino IA #34	104/78	38.6
39	1	2	Dados sintéticos para treino IA #35	106/64	37.4
40	1	4	Dados sintéticos para treino IA #36	105/88	38.2
41	1	4	Dados sintéticos para treino IA #37	101/74	39.4
42	1	3	Dados sintéticos para treino IA #38	126/74	37.6
43	1	3	Dados sintéticos para treino IA #39	100/90	36.5
44	1	5	Dados sintéticos para treino IA #40	110/83	36.8
45	1	5	Dados sintéticos para treino IA #41	113/61	38.1
46	1	3	Dados sintéticos para treino IA #42	137/82	38.5
47	1	3	Dados sintéticos para treino IA #43	114/68	36.6
48	1	5	Dados sintéticos para treino IA #44	113/63	38
49	1	4	Dados sintéticos para treino IA #45	109/74	39.4
50	1	3	Dados sintéticos para treino IA #46	128/67	39.5
51	1	5	Dados sintéticos para treino IA #47	112/83	39.3
52	1	4	Dados sintéticos para treino IA #48	138/75	36.3
53	1	3	Dados sintéticos para treino IA #49	124/89	36.1
54	1	5	Dados sintéticos para treino IA #50	133/69	37.9
55	1	3	Dados sintéticos para treino IA #51	107/63	36.9
56	1	4	Dados sintéticos para treino IA #52	117/87	36.7
57	1	4	Dados sintéticos para treino IA #53	116/83	38.9
58	1	3	Dados sintéticos para treino IA #54	103/83	39.5
59	1	4	Dados sintéticos para treino IA #55	135/66	37.3
60	1	1	Dados sintéticos para treino IA #56	135/79	38.9
61	1	4	Dados sintéticos para treino IA #57	137/80	36.2
62	1	4	Dados sintéticos para treino IA #58	131/78	38.7
63	1	4	Dados sintéticos para treino IA #59	114/63	36.2
64	1	4	Dados sintéticos para treino IA #60	137/75	36.5
65	1	3	Dados sintéticos para treino IA #61	102/79	36.9
66	1	5	Dados sintéticos para treino IA #62	101/73	38.2
67	1	5	Dados sintéticos para treino IA #63	115/82	39.3
68	1	5	Dados sintéticos para treino IA #64	126/73	36.7
69	1	5	Dados sintéticos para treino IA #65	126/79	37.1
70	1	4	Dados sintéticos para treino IA #66	139/73	37.7
71	1	4	Dados sintéticos para treino IA #67	101/78	38
72	1	2	Dados sintéticos para treino IA #68	128/84	38.5
73	1	2	Dados sintéticos para treino IA #69	103/72	38.4
74	1	2	Dados sintéticos para treino IA #70	122/70	38.5
75	1	3	Dados sintéticos para treino IA #71	108/82	38.9
76	1	3	Dados sintéticos para treino IA #72	101/84	38.7
77	1	3	Dados sintéticos para treino IA #73	133/76	36.4
78	1	5	Dados sintéticos para treino IA #74	116/64	38.6
79	1	3	Dados sintéticos para treino IA #75	107/73	36.6
80	1	3	Dados sintéticos para treino IA #76	120/78	37.6
81	1	3	Dados sintéticos para treino IA #77	131/82	38.1
82	1	3	Dados sintéticos para treino IA #78	123/90	37.5
83	1	4	Dados sintéticos para treino IA #79	132/62	38.8
84	1	3	Dados sintéticos para treino IA #80	135/71	36.3
85	1	3	Traumatismo craniano	100/79	36.8
87	1	4	Fratura suspeita no braço	109/84	37
88	1	2	Vómitos persistentes	137/75	37
90	1	1	Crise de asma	122/69	38.4
91	1	4	Corte profundo na mão	132/78	38.2
92	1	3	Dor no peito	107/61	36.4
93	1	2	Dor abdominal intensa	128/90	38.3
94	1	2	Dor no peito	116/87	38.8
95	1	1	Fratura suspeita no braço	130/65	36.6
96	1	4	Crise de asma	130/86	37.9
97	1	3	Dificuldade respiratória	119/65	38.2
98	1	5	Febre alta (39.5ºC)	124/82	38
99	1	2	Febre alta (39.5ºC)	106/64	37.6
100	1	1	Febre alta (39.5ºC)	111/85	37.3
102	1	1	Dor no peito	107/88	38.3
103	1	5	Febre alta (39.5ºC)	132/83	38.2
104	1	5	Dificuldade respiratória	107/87	36.1
105	1	4	Corte profundo na mão	126/67	36.5
106	1	1	Dor lombar aguda	119/71	38
108	1	2	Dificuldade respiratória	120/83	37.5
109	1	3	Alergia grave	121/67	38.3
112	1	5	Traumatismo craniano	138/61	38.8
113	1	5	Febre alta (39.5ºC)	139/84	36.7
115	1	2	Vómitos persistentes	124/72	38.2
116	1	5	Dor abdominal intensa	121/73	37.5
117	1	1	Fratura suspeita no braço	127/61	38.7
118	1	3	Traumatismo craniano	113/87	36
119	1	4	Dor abdominal intensa	107/62	39.2
121	1	2	Dor lombar aguda	109/75	36.7
122	1	2	Dor abdominal intensa	122/72	39.3
124	1	4	Dor no peito	116/83	36.2
125	1	4	Febre alta (39.5ºC)	137/79	36.8
126	1	3	Dor abdominal intensa	103/89	37.1
127	1	5	Vómitos persistentes	103/79	38
128	1	4	Tontura e desequilíbrio	139/70	38.1
129	1	4	Corte profundo na mão	123/69	36.3
130	1	1	Dor abdominal intensa	136/88	38.3
132	1	5	Dor abdominal intensa	103/90	37.8
133	1	3	Corte profundo na mão	127/86	37.4
134	1	4	Crise de asma	127/89	37.2
135	1	4	Alergia grave	108/61	37.6
136	1	1	Corte profundo na mão	116/73	37.5
137	1	3	Alergia grave	102/67	39.1
138	1	4	Fratura suspeita no braço	104/61	38.4
139	1	3	Febre alta (39.5ºC)	116/90	39
140	1	1	Traumatismo craniano	129/77	37.8
141	1	1	Vómitos persistentes	127/88	38.6
142	1	3	Traumatismo craniano	138/70	37.1
143	1	2	Fratura suspeita no braço	102/63	39.2
144	1	1	Fratura suspeita no braço	109/86	36.4
145	1	5	Corte profundo na mão	135/66	37.2
147	1	5	Crise de asma	138/81	36.5
148	1	1	Dificuldade respiratória	130/61	36.1
149	1	1	Dor no peito	113/65	39.3
150	1	5	Tontura e desequilíbrio	135/62	37.4
151	1	5	Vómitos persistentes	110/79	37
152	1	3	Alergia grave	110/83	39.5
153	1	5	Fratura suspeita no braço	117/89	38.9
154	1	2	Febre alta (39.5ºC)	100/71	36.6
155	1	5	Dor abdominal intensa	106/82	38.3
156	1	5	Tontura e desequilíbrio	135/72	37.6
158	1	4	Dor abdominal intensa	119/81	39.5
159	1	2	Dor abdominal intensa	131/64	37.4
160	1	3	Febre alta (39.5ºC)	104/88	37.8
161	1	5	Tontura e desequilíbrio	125/64	38.1
162	1	4	Crise de asma	122/63	38.6
163	1	3	Crise de asma	111/73	37.8
164	1	1	Vómitos persistentes	108/74	38
165	1	1	Dor no peito	114/82	38.1
167	1	2	Febre alta (39.5ºC)	127/80	38.5
168	1	4	Tontura e desequilíbrio	128/86	36.1
169	1	1	Dor no peito	124/62	37.4
170	1	2	Tontura e desequilíbrio	133/85	36.8
171	1	3	Crise de asma	101/71	37.2
174	1	2	Tontura e desequilíbrio	121/84	36.6
175	1	4	Crise de asma	137/90	38.3
176	1	5	Crise de asma	131/82	39
179	1	4	Crise de asma	122/90	38.5
180	1	3	Febre alta (39.5ºC)	104/87	38.1
181	1	4	Corte profundo na mão	116/73	38.1
182	1	1	Traumatismo craniano	100/89	39.2
183	1	2	Crise de asma	120/72	36.6
185	1	5	Dor lombar aguda	115/80	36.8
186	1	5	Traumatismo craniano	106/70	39.3
187	1	5	Dificuldade respiratória	113/71	38.1
188	1	5	Febre alta (39.5ºC)	139/76	36.8
189	1	5	Dor lombar aguda	126/87	39.1
190	1	3	Vómitos persistentes	103/73	37.3
191	1	5	Traumatismo craniano	138/61	38
192	1	3	Vómitos persistentes	126/72	36.4
193	1	5	Fratura suspeita no braço	115/90	37.7
194	1	3	Dor no peito	103/85	36.3
196	1	1	Dor lombar aguda	133/72	38.9
197	1	3	Dor lombar aguda	137/66	38.4
199	1	5	Tontura e desequilíbrio	125/88	36.1
200	1	2	Dor abdominal intensa	113/87	38.6
201	1	1	Corte profundo na mão	113/67	37.6
202	1	2	Traumatismo craniano	118/83	38.9
203	1	1	Crise de asma	121/70	39.5
204	1	4	Traumatismo craniano	106/70	36.6
\.


--
-- Data for Name: utilizador; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.utilizador (idutilizador, username, passwordhash, idperfil) FROM stdin;
1	dr.silva	$2b$12$0AaT8CuuMcSAwadAPvEBkekaV3Rk77uHpNizProTLA8/xSChEPl1.	1
2	enf.ana	$2b$12$AAWDO.hCsEPOLA6amyXbue5gT0XjxpHUn80RddJhLuZpiLxtCplCu	2
3	rec.joao	$2b$12$zGNwZ..mJemyS273OupoiOsLK3QwlhfXlZDPJkfO2gnTnlX.JiaE6	3
4	admin	$2b$12$h9anDAc2ObImWL642biZX.r8izi4cZqhskynsJanDxLoXyUQudBMy	4
\.


--
-- Name: ato_idato_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ato_idato_seq', 71, true);


--
-- Name: episodio_numepis_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.episodio_numepis_seq', 204, true);


--
-- Name: funcionario_idfuncionario_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.funcionario_idfuncionario_seq', 2, true);


--
-- Name: prescricao_idprescricao_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.prescricao_idprescricao_seq', 70, true);


--
-- Name: t1_utente_numutente_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.t1_utente_numutente_seq', 1, false);


--
-- Name: tipoato_idtipoato_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tipoato_idtipoato_seq', 1, false);


--
-- Name: utilizador_idutilizador_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.utilizador_idutilizador_seq', 4, true);


--
-- Name: ato ato_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ato
    ADD CONSTRAINT ato_pkey PRIMARY KEY (idato);


--
-- Name: enfermeiro enfermeiro_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enfermeiro
    ADD CONSTRAINT enfermeiro_pkey PRIMARY KEY (enfnumfunc);


--
-- Name: episodio episodio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.episodio
    ADD CONSTRAINT episodio_pkey PRIMARY KEY (numepis);


--
-- Name: funcionario funcionario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionario
    ADD CONSTRAINT funcionario_pkey PRIMARY KEY (idfuncionario);


--
-- Name: hospital hospital_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hospital
    ADD CONSTRAINT hospital_pkey PRIMARY KEY (nomehosp);


--
-- Name: internamento internamento_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.internamento
    ADD CONSTRAINT internamento_pkey PRIMARY KEY (numepis);


--
-- Name: medico medico_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medico
    ADD CONSTRAINT medico_pkey PRIMARY KEY (mednumfunc);


--
-- Name: prescricao prescricao_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescricao
    ADD CONSTRAINT prescricao_pkey PRIMARY KEY (idprescricao);


--
-- Name: t1_utente t1_utente_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t1_utente
    ADD CONSTRAINT t1_utente_pkey PRIMARY KEY (numutente);


--
-- Name: tipoato tipoato_designacao_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipoato
    ADD CONSTRAINT tipoato_designacao_key UNIQUE (designacao);


--
-- Name: tipoato tipoato_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tipoato
    ADD CONSTRAINT tipoato_pkey PRIMARY KEY (idtipoato);


--
-- Name: triagem triagem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triagem
    ADD CONSTRAINT triagem_pkey PRIMARY KEY (numepis);


--
-- Name: utilizador utilizador_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.utilizador
    ADD CONSTRAINT utilizador_pkey PRIMARY KEY (idutilizador);


--
-- Name: utilizador utilizador_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.utilizador
    ADD CONSTRAINT utilizador_username_key UNIQUE (username);


--
-- Name: ato ato_idtipoato_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ato
    ADD CONSTRAINT ato_idtipoato_fkey FOREIGN KEY (idtipoato) REFERENCES public.tipoato(idtipoato);


--
-- Name: ato ato_mednumfunc_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ato
    ADD CONSTRAINT ato_mednumfunc_fkey FOREIGN KEY (mednumfunc) REFERENCES public.medico(mednumfunc);


--
-- Name: ato ato_numepis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ato
    ADD CONSTRAINT ato_numepis_fkey FOREIGN KEY (numepis) REFERENCES public.episodio(numepis);


--
-- Name: enfermeiro enfermeiro_enfnumfunc_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enfermeiro
    ADD CONSTRAINT enfermeiro_enfnumfunc_fkey FOREIGN KEY (enfnumfunc) REFERENCES public.funcionario(idfuncionario);


--
-- Name: episodio episodio_nomehosp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.episodio
    ADD CONSTRAINT episodio_nomehosp_fkey FOREIGN KEY (nomehosp) REFERENCES public.hospital(nomehosp);


--
-- Name: episodio episodio_numutente_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.episodio
    ADD CONSTRAINT episodio_numutente_fkey FOREIGN KEY (numutente) REFERENCES public.t1_utente(numutente);


--
-- Name: funcionario funcionario_idutilizador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionario
    ADD CONSTRAINT funcionario_idutilizador_fkey FOREIGN KEY (idutilizador) REFERENCES public.utilizador(idutilizador);


--
-- Name: funcionario funcionario_nomehosp_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.funcionario
    ADD CONSTRAINT funcionario_nomehosp_fkey FOREIGN KEY (nomehosp) REFERENCES public.hospital(nomehosp);


--
-- Name: internamento internamento_numepis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.internamento
    ADD CONSTRAINT internamento_numepis_fkey FOREIGN KEY (numepis) REFERENCES public.episodio(numepis);


--
-- Name: medico medico_mednumfunc_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medico
    ADD CONSTRAINT medico_mednumfunc_fkey FOREIGN KEY (mednumfunc) REFERENCES public.funcionario(idfuncionario);


--
-- Name: prescricao prescricao_mednumfunc_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescricao
    ADD CONSTRAINT prescricao_mednumfunc_fkey FOREIGN KEY (mednumfunc) REFERENCES public.medico(mednumfunc);


--
-- Name: prescricao prescricao_numepis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prescricao
    ADD CONSTRAINT prescricao_numepis_fkey FOREIGN KEY (numepis) REFERENCES public.episodio(numepis);


--
-- Name: triagem triagem_enfnumfunc_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triagem
    ADD CONSTRAINT triagem_enfnumfunc_fkey FOREIGN KEY (enfnumfunc) REFERENCES public.enfermeiro(enfnumfunc);


--
-- Name: triagem triagem_numepis_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triagem
    ADD CONSTRAINT triagem_numepis_fkey FOREIGN KEY (numepis) REFERENCES public.episodio(numepis);


--
-- PostgreSQL database dump complete
--

\unrestrict rruuR4qjluxkp371xQPjctqdyI3KypbPYzsUAnYE8b2AiNJ13uFNK6pjcmtx4nO

