--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.5 (Postgres-XL 9.5r1.4)
-- Dumped by pg_dump version 9.5.5 (Postgres-XL 9.5r1.4)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
)
DISTRIBUTE BY REPLICATION;


ALTER TABLE auth_group OWNER TO tsdp;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO tsdp;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE auth_group_permissions OWNER TO tsdp;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO tsdp;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE auth_permission OWNER TO tsdp;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO tsdp;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
)
DISTRIBUTE BY REPLICATION;


ALTER TABLE auth_user OWNER TO tsdp;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE auth_user_groups OWNER TO tsdp;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO tsdp;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO tsdp;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE auth_user_user_permissions OWNER TO tsdp;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO tsdp;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
)
DISTRIBUTE BY HASH (id);


ALTER TABLE django_admin_log OWNER TO tsdp;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO tsdp;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE django_content_type OWNER TO tsdp;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO tsdp;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE django_migrations OWNER TO tsdp;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO tsdp;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
)
DISTRIBUTE BY HASH (session_key);


ALTER TABLE django_session OWNER TO tsdp;

--
-- Name: feed_bidask; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE feed_bidask (
    id integer NOT NULL,
    frequency integer,
    ask double precision,
    asksize double precision,
    bid double precision,
    bidsize double precision,
    date timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    crawl_source character varying(200),
    instrument_id integer NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE feed_bidask OWNER TO tsdp;

--
-- Name: feed_bidask_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE feed_bidask_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feed_bidask_id_seq OWNER TO tsdp;

--
-- Name: feed_bidask_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE feed_bidask_id_seq OWNED BY feed_bidask.id;


--
-- Name: feed_feed; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE feed_feed (
    id integer NOT NULL,
    frequency integer,
    date timestamp with time zone,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    change double precision,
    settle double precision,
    open_interest double precision,
    volume double precision,
    wap double precision,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    crawl_source character varying(200),
    instrument_id integer NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE feed_feed OWNER TO tsdp;

--
-- Name: feed_feed_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE feed_feed_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feed_feed_id_seq OWNER TO tsdp;

--
-- Name: feed_feed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE feed_feed_id_seq OWNED BY feed_feed.id;


--
-- Name: feed_instrument; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE feed_instrument (
    id integer NOT NULL,
    broker character varying(255),
    sym character varying(255),
    cur character varying(255),
    exch character varying(255),
    "secType" character varying(255),
    trade_freq integer,
    mult double precision,
    local_sym character varying(255),
    "contractMonth" character varying(255),
    expiry character varying(255),
    "evRule" character varying(255),
    "liquidHours" character varying(255),
    "longName" character varying(255),
    "minTick" double precision,
    "timeZoneId" character varying(255),
    "tradingHours" character varying(255),
    "underConId" integer,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    crawl_source character varying(200),
    resource_id integer
)
DISTRIBUTE BY HASH (id);


ALTER TABLE feed_instrument OWNER TO tsdp;

--
-- Name: feed_instrument_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE feed_instrument_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feed_instrument_id_seq OWNER TO tsdp;

--
-- Name: feed_instrument_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE feed_instrument_id_seq OWNED BY feed_instrument.id;


--
-- Name: feed_prediction; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE feed_prediction (
    id integer NOT NULL,
    frequency integer,
    pred_start_date timestamp with time zone,
    date timestamp with time zone,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    wap double precision,
    algo_name character varying(200),
    is_scaled boolean NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    crawl_source character varying(200),
    instrument_id integer NOT NULL
)
DISTRIBUTE BY HASH (id);


ALTER TABLE feed_prediction OWNER TO tsdp;

--
-- Name: feed_prediction_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE feed_prediction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feed_prediction_id_seq OWNER TO tsdp;

--
-- Name: feed_prediction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE feed_prediction_id_seq OWNED BY feed_prediction.id;


--
-- Name: feed_resource; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE feed_resource (
    id integer NOT NULL,
    resource_type character varying(50) NOT NULL,
    commodity_type character varying(50) NOT NULL,
    is_active boolean NOT NULL,
    is_commodity boolean NOT NULL,
    is_public boolean NOT NULL,
    ticker character varying(100),
    exchange character varying(100),
    sec_cik character varying(100),
    sec_cik_int character varying(100),
    partner_order integer NOT NULL,
    company_name character varying(500) NOT NULL,
    last_edited_time timestamp with time zone NOT NULL,
    created_time timestamp with time zone
)
DISTRIBUTE BY HASH (id);


ALTER TABLE feed_resource OWNER TO tsdp;

--
-- Name: feed_resource_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE feed_resource_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feed_resource_id_seq OWNER TO tsdp;

--
-- Name: feed_resource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE feed_resource_id_seq OWNED BY feed_resource.id;


--
-- Name: feed_system; Type: TABLE; Schema: public; Owner: tsdp
--

CREATE TABLE feed_system (
    id integer NOT NULL,
    version character varying(255),
    system character varying(255),
    name character varying(255),
    c2id character varying(255),
    c2api character varying(255),
    c2qty integer,
    c2submit boolean NOT NULL,
    ibqty integer,
    ibsubmit boolean NOT NULL,
    trade_freq integer,
    ibmult integer,
    c2mult integer,
    signal character varying(255),
    c2instrument_id integer,
    ibinstrument_id integer
)
DISTRIBUTE BY HASH (id);


ALTER TABLE feed_system OWNER TO tsdp;

--
-- Name: feed_system_id_seq; Type: SEQUENCE; Schema: public; Owner: tsdp
--

CREATE SEQUENCE feed_system_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feed_system_id_seq OWNER TO tsdp;

--
-- Name: feed_system_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tsdp
--

ALTER SEQUENCE feed_system_id_seq OWNED BY feed_system.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_bidask ALTER COLUMN id SET DEFAULT nextval('feed_bidask_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_feed ALTER COLUMN id SET DEFAULT nextval('feed_feed_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_instrument ALTER COLUMN id SET DEFAULT nextval('feed_instrument_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_prediction ALTER COLUMN id SET DEFAULT nextval('feed_prediction_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_resource ALTER COLUMN id SET DEFAULT nextval('feed_resource_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_system ALTER COLUMN id SET DEFAULT nextval('feed_system_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
8	Can change group	3	change_group
9	Can delete group	3	delete_group
12	Can delete user	4	delete_user
17	Can change content type	6	change_contenttype
13	Can add session	5	add_session
15	Can delete session	5	delete_session
19	Can add resource	7	add_resource
21	Can delete resource	7	delete_resource
23	Can change instrument	9	change_instrument
26	Can change system	11	change_system
28	Can add feed	8	add_feed
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
7	Can add group	3	add_group
10	Can add user	4	add_user
11	Can change user	4	change_user
16	Can add content type	6	add_contenttype
18	Can delete content type	6	delete_contenttype
14	Can change session	5	change_session
20	Can change resource	7	change_resource
22	Can add instrument	9	add_instrument
24	Can delete instrument	9	delete_instrument
25	Can add system	11	add_system
27	Can delete system	11	delete_system
29	Can change feed	8	change_feed
30	Can delete feed	8	delete_feed
31	Can add prediction	12	add_prediction
32	Can change prediction	12	change_prediction
33	Can delete prediction	12	delete_prediction
34	Can add bid ask	13	add_bidask
35	Can change bid ask	13	change_bidask
36	Can delete bid ask	13	delete_bidask
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('auth_permission_id_seq', 47, false);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, false);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
6	contenttypes	contenttype
5	sessions	session
9	feed	instrument
8	feed	feed
12	feed	prediction
13	feed	bidask
3	auth	group
4	auth	user
7	feed	resource
11	feed	system
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('django_content_type_id_seq', 15, false);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-03-08 17:14:51.254957+07
2	auth	0001_initial	2017-03-08 17:14:51.375062+07
5	admin	0002_logentry_remove_auto_add	2017-03-08 17:14:51.460345+07
6	contenttypes	0002_remove_content_type_name	2017-03-08 17:14:51.507726+07
8	auth	0002_alter_permission_name_max_length	2017-03-08 17:14:51.550773+07
9	auth	0003_alter_user_email_max_length	2017-03-08 17:14:51.593336+07
13	auth	0006_require_contenttypes_0002	2017-03-08 17:14:51.717446+07
12	auth	0007_alter_validators_add_error_messages	2017-03-08 17:14:51.757556+07
3	admin	0001_initial	2017-03-08 17:14:51.423782+07
10	auth	0004_alter_user_username_opts	2017-03-08 17:14:51.627462+07
11	auth	0005_alter_user_last_login_null	2017-03-08 17:14:51.679404+07
4	feed	0001_initial	2017-03-08 17:14:51.795306+07
7	sessions	0001_initial	2017-03-08 17:14:51.834735+07
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('django_migrations_id_seq', 17, false);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: feed_bidask; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY feed_bidask (id, frequency, ask, asksize, bid, bidsize, date, created_at, updated_at, crawl_source, instrument_id) FROM stdin;
\.


--
-- Name: feed_bidask_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('feed_bidask_id_seq', 1, false);


--
-- Data for Name: feed_feed; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY feed_feed (id, frequency, date, open, high, low, close, change, settle, open_interest, volume, wap, created_at, updated_at, crawl_source, instrument_id) FROM stdin;
\.


--
-- Name: feed_feed_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('feed_feed_id_seq', 1, false);


--
-- Data for Name: feed_instrument; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY feed_instrument (id, broker, sym, cur, exch, "secType", trade_freq, mult, local_sym, "contractMonth", expiry, "evRule", "liquidHours", "longName", "minTick", "timeZoneId", "tradingHours", "underConId", created_at, updated_at, crawl_source, resource_id) FROM stdin;
1	ib	EMD	USD	GLOBEX	FUT	\N	0	EMD	201612	20161216		20161116:0830-1515,1530-1600;20161117:0830-1515,1530-1600	E-mini S&P Midcap 400 Futures	0.100000000000000006	CST	20161116:1700-1515,1530-1600;20161117:1700-1515,1530-1600	14218823	2017-03-08 17:22:54.511274+07	2017-03-08 17:22:54.511295+07		\N
2	ib	YM	USD	ECBOT	FUT	\N	0	YM	201612	20161216		20161116:0830-1515,1530-1600;20161117:0830-1515,1530-1600	Mini Sized Dow Jones Industrial Average $5	1	CST	20161116:1700-1515,1530-1600;20161117:1700-1515,1530-1600	14721310	2017-03-08 17:22:54.574529+07	2017-03-08 17:22:54.574608+07		\N
5	ib	HG	USD	NYMEX	FUT	\N	0	HG	201612	20161228		20161116:0930-1700;20161117:0930-1700	NYMEX Copper Index	0.00050000000000000001	EST5EDT	20161116:1800-1700;20161117:1800-1700	36557087	2017-03-08 17:22:54.736794+07	2017-03-08 17:22:54.73688+07		\N
6	ib	HE	USD	GLOBEX	FUT	\N	0	HE	201702	20170214		20161116:0830-1305;20161117:0830-1305	Lean Hogs	0.000250000000000000005	CST	20161116:0830-1305;20161117:0830-1305	32612382	2017-03-08 17:22:54.79438+07	2017-03-08 17:22:54.794503+07		\N
9	ib	ZS	USD	ECBOT	FUT	\N	0	ZS	201701	20170113		20161116:0830-1320;20161117:0830-1320	Soybean Futures	0.00250000000000000005	CST	20161116:1900-0745,0830-1320;20161117:1900-0745,0830-1320	11160664	2017-03-08 17:22:54.889566+07	2017-03-08 17:22:54.889616+07		\N
13	ib	PA	USD	NYMEX	FUT	\N	0	PA	201612	20161228		20161116:0930-1700;20161117:0930-1700	NYMEX Palladium Index	0.0500000000000000028	EST5EDT	20161116:1800-1700;20161117:1800-1700	36557097	2017-03-08 17:22:54.974594+07	2017-03-08 17:22:54.974671+07		\N
12	ib	CAD	USD	GLOBEX	FUT	\N	0	CAD	201612	20161220		20161116:0830-1600;20161117:0830-1600	CAD.USD Forex	5.00000000000000024e-05	CST	20161116:1700-1600;20161117:1700-1600	15016251	2017-03-08 17:22:55.141059+07	2017-03-08 17:22:55.141138+07		\N
15	ib	PL	USD	NYMEX	FUT	\N	0	PL	201701	20170127		20161116:0930-1700;20161117:0930-1700	NYMEX Platinum Index	0.100000000000000006	EST5EDT	20161116:1800-1700;20161117:1800-1700	36557100	2017-03-08 17:22:55.185757+07	2017-03-08 17:22:55.185839+07		\N
8	ib	ZM	USD	ECBOT	FUT	\N	0	ZM	201612	20161214		20161116:0830-1320;20161117:0830-1320	Soybean Meal Futures	0.100000000000000006	CST	20161116:1900-0745,0830-1320;20161117:1900-0745,0830-1320	11160676	2017-03-08 17:22:55.305629+07	2017-03-08 17:22:55.305705+07		\N
17	ib	ZN	USD	ECBOT	FUT	\N	0	ZN	201612	20161220		20161116:0830-1600;20161117:0830-1600	10 Year US Treasury Note	0.015625	CST	20161116:1700-1600;20161117:1700-1600	11078390	2017-03-08 17:22:55.365861+07	2017-03-08 17:22:55.365935+07		\N
19	ib	AUD	USD	GLOBEX	FUT	\N	0	AUD	201612	20161219		20161116:0830-1600;20161117:0830-1600	Australian dollar	0.000100000000000000005	CST	20161116:1700-1600;20161117:1700-1600	14433401	2017-03-08 17:22:55.420073+07	2017-03-08 17:22:55.420152+07		\N
23	ib	CL	USD	NYMEX	FUT	\N	0	CL	201701	20161220		20161116:0930-1700;20161117:0930-1700	Light Sweet Crude Oil	0.0100000000000000002	EST5EDT	20161116:1800-1700;20161117:1800-1700	17340715	2017-03-08 17:22:55.553279+07	2017-03-08 17:22:55.553398+07		\N
40	ib	NZD	USD	GLOBEX	FUT	\N	0	NZD	201612	20161219		20161116:0830-1600;20161117:0830-1600	New Zealand dollar	0.000100000000000000005	CST	20161116:1700-1600;20161117:1700-1600	39453441	2017-03-08 17:22:55.905994+07	2017-03-08 17:22:55.906072+07		\N
26	ib	ZW	USD	ECBOT	FUT	\N	0	ZW	201612	20161214		20161116:0830-1320;20161117:0830-1320	Wheat Futures	0.00250000000000000005	CST	20161116:1900-0745,0830-1320;20161117:1900-0745,0830-1320	11160683	2017-03-08 17:22:56.038931+07	2017-03-08 17:22:56.039067+07		\N
21	ib	ES	USD	GLOBEX	FUT	\N	0	ES	201612	20161216		20161116:0830-1515,1530-1600;20161117:0830-1515,1530-1600	E-mini S&P 500	0.25	CST	20161116:1700-1515,1530-1600;20161117:1700-1515,1530-1600	11004968	2017-03-08 17:22:56.102203+07	2017-03-08 17:22:56.102382+07		\N
41	ib	EUR	USD	GLOBEX	FUT	\N	0	EUR	201612	20161219		20161116:0830-1600;20161117:0830-1600	European Monetary Union Euro	5.00000000000000024e-05	CST	20161116:1700-1600;20161117:1700-1600	12087792	2017-03-08 17:22:56.161624+07	2017-03-08 17:22:56.161702+07		\N
42	ib	JPY	USD	GLOBEX	FUT	\N	0	JPY	201612	20161219		20161116:0830-1600;20161117:0830-1600	JPY.USD Forex	4.99999999999999977e-07	CST	20161116:1700-1600;20161117:1700-1600	15016105	2017-03-08 17:22:56.26328+07	2017-03-08 17:22:56.263396+07		\N
28	ib	SI	USD	NYMEX	FUT	\N	0	SI	201612	20161228		20161116:0930-1700;20161117:0930-1700	NYMEX Silver Index	0.0050000000000000001	EST5EDT	20161116:1800-1700;20161117:1800-1700	36557082	2017-03-08 17:22:56.308766+07	2017-03-08 17:22:56.308846+07		\N
3	ib	HO	USD	NYMEX	FUT	\N	0	HO	201701	20161230		20161116:0930-1700;20161117:0930-1700	Heating Oil	0.000100000000000000005	EST5EDT	20161116:1800-1700;20161117:1800-1700	36552987	2017-03-08 17:22:54.649881+07	2017-03-08 17:22:54.650001+07		\N
4	ib	GBP	USD	GLOBEX	FUT	\N	0	GBP	201612	20161219		20161116:0830-1600;20161117:0830-1600	British pound	0.000100000000000000005	CST	20161116:1700-1600;20161117:1700-1600	12087797	2017-03-08 17:22:54.702145+07	2017-03-08 17:22:54.702214+07		\N
7	ib	LE	USD	GLOBEX	FUT	\N	0	LE	201702	20170228		20161116:0830-1305;20161117:0830-1305	Live Cattle	0.000250000000000000005	CST	20161116:0830-1305;20161117:0830-1305	33221066	2017-03-08 17:22:54.841499+07	2017-03-08 17:22:54.841522+07		\N
10	ib	NG	USD	NYMEX	FUT	\N	0	NG	201701	20161228		20161116:0930-1700;20161117:0930-1700	Henry Hub Natural Gas	0.00100000000000000002	EST5EDT	20161116:1800-1700;20161117:1800-1700	36552980	2017-03-08 17:22:54.927062+07	2017-03-08 17:22:54.927122+07		\N
11	ib	RB	USD	NYMEX	FUT	\N	0	RB	201701	20161230		20161116:0930-1700;20161117:0930-1700	NYMEX RBOB Gasoline Index	0.000100000000000000005	EST5EDT	20161116:1800-1700;20161117:1800-1700	36586917	2017-03-08 17:22:55.02969+07	2017-03-08 17:22:55.029815+07		\N
14	ib	NQ	USD	GLOBEX	FUT	\N	0	NQ	201612	20161216		20161116:0830-1515,1530-1600;20161117:0830-1515,1530-1600	E-mini NASDAQ 100 Futures	0.25	CST	20161116:1700-1515,1530-1600;20161117:1700-1515,1530-1600	11004958	2017-03-08 17:22:55.087156+07	2017-03-08 17:22:55.087236+07		\N
16	ib	ZL	USD	ECBOT	FUT	\N	0	ZL	201612	20161214		20161116:0830-1320;20161117:0830-1320	Soybean Oil Futures	0.000100000000000000005	CST	20161116:1900-0745,0830-1320;20161117:1900-0745,0830-1320	11160669	2017-03-08 17:22:55.241642+07	2017-03-08 17:22:55.241721+07		\N
18	ib	CHF	USD	GLOBEX	FUT	\N	0	CHF	201612	20161219		20161116:0830-1600;20161117:0830-1600	Swiss franc	0.000100000000000000005	CST	20161116:1700-1600;20161117:1700-1600	12087802	2017-03-08 17:22:55.475635+07	2017-03-08 17:22:55.475743+07		\N
31	ib	ZF	USD	ECBOT	FUT	\N	0	ZF	201612	20161230		20161116:0830-1600;20161117:0830-1600	5 Year US Treasury Note	0.0078125	CST	20161116:1700-1600;20161117:1700-1600	11078387	2017-03-08 17:22:55.606659+07	2017-03-08 17:22:55.60674+07		\N
20	ib	ZB	USD	ECBOT	FUT	\N	0	ZB	201612	20161220		20161116:0830-1600;20161117:0830-1600	30 Year US Treasury Bond	0.03125	CST	20161116:1700-1600;20161117:1700-1600	11078381	2017-03-08 17:22:55.662561+07	2017-03-08 17:22:55.662637+07		\N
39	ib	ZC	USD	ECBOT	FUT	\N	0	ZC	201703	20170314		20161116:0830-1320;20161117:0830-1320	Corn Futures	0.00250000000000000005	CST	20161116:1900-0745,0830-1320;20161117:1900-0745,0830-1320	11160400	2017-03-08 17:22:55.721481+07	2017-03-08 17:22:55.721559+07		\N
24	ib	GF	USD	GLOBEX	FUT	\N	0	GF	201701	20170126		20161116:0830-1305;20161117:0830-1305	Feeder Cattle	0.000250000000000000005	CST	20161116:0830-1305;20161117:0830-1305	32612420	2017-03-08 17:22:55.794634+07	2017-03-08 17:22:55.794736+07		\N
32	ib	GC	USD	NYMEX	FUT	\N	0	GC	201612	20161228		20161116:0930-1700;20161117:0930-1700	Gold	0.100000000000000006	EST5EDT	20161116:1800-1700;20161117:1800-1700	17340718	2017-03-08 17:22:55.841041+07	2017-03-08 17:22:55.841118+07		\N
25	ib	ZT	USD	ECBOT	FUT	\N	0	ZT	201612	20161230		20161116:0830-1600;20161117:0830-1600	2 Year US Treasury Note	0.0078125	CST	20161116:1700-1600;20161117:1700-1600	11160388	2017-03-08 17:22:55.967811+07	2017-03-08 17:22:55.96804+07		\N
27	ib	MXP	USD	GLOBEX	FUT	\N	0	MXP	201612	20161219		20161116:0830-1600;20161117:0830-1600	MXP.USD Forex	1.00000000000000008e-05	CST	20161116:1700-1600;20161117:1700-1600	35045201	2017-03-08 17:22:56.221139+07	2017-03-08 17:22:56.221259+07		\N
22	ib	NIY	JPY	GLOBEX	FUT	\N	0	NIY	201612	20161208		20161116:0830-1600;20161117:0830-1600	Yen Denominated Nikkei 225 Index	5	CST	20161116:1700-1600;20161117:1700-1600	28001490	2017-03-08 17:22:56.374396+07	2017-03-08 17:22:56.374514+07		\N
\.


--
-- Name: feed_instrument_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('feed_instrument_id_seq', 46, false);


--
-- Data for Name: feed_prediction; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY feed_prediction (id, frequency, pred_start_date, date, open, high, low, close, volume, wap, algo_name, is_scaled, created_at, updated_at, crawl_source, instrument_id) FROM stdin;
\.


--
-- Name: feed_prediction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('feed_prediction_id_seq', 1, false);


--
-- Data for Name: feed_resource; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY feed_resource (id, resource_type, commodity_type, is_active, is_commodity, is_public, ticker, exchange, sec_cik, sec_cik_int, partner_order, company_name, last_edited_time, created_time) FROM stdin;
\.


--
-- Name: feed_resource_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('feed_resource_id_seq', 1, false);


--
-- Data for Name: feed_system; Type: TABLE DATA; Schema: public; Owner: tsdp
--

COPY feed_system (id, version, system, name, c2id, c2api, c2qty, c2submit, ibqty, ibsubmit, trade_freq, ibmult, c2mult, signal, c2instrument_id, ibinstrument_id) FROM stdin;
\.


--
-- Name: feed_system_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tsdp
--

SELECT pg_catalog.setval('feed_system_id_seq', 1, false);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: feed_bidask_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_bidask
    ADD CONSTRAINT feed_bidask_pkey PRIMARY KEY (id);


--
-- Name: feed_feed_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_feed
    ADD CONSTRAINT feed_feed_pkey PRIMARY KEY (id);


--
-- Name: feed_instrument_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_instrument
    ADD CONSTRAINT feed_instrument_pkey PRIMARY KEY (id);


--
-- Name: feed_prediction_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_prediction
    ADD CONSTRAINT feed_prediction_pkey PRIMARY KEY (id);


--
-- Name: feed_resource_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_resource
    ADD CONSTRAINT feed_resource_pkey PRIMARY KEY (id);


--
-- Name: feed_system_pkey; Type: CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY feed_system
    ADD CONSTRAINT feed_system_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: feed_bidask_5fc73231; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_bidask_5fc73231 ON feed_bidask USING btree (date);


--
-- Name: feed_bidask_9afea17b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_bidask_9afea17b ON feed_bidask USING btree (instrument_id);


--
-- Name: feed_bidask_afd1a1a8; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_bidask_afd1a1a8 ON feed_bidask USING btree (updated_at);


--
-- Name: feed_bidask_fad6c43b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_bidask_fad6c43b ON feed_bidask USING btree (frequency);


--
-- Name: feed_bidask_fde81f11; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_bidask_fde81f11 ON feed_bidask USING btree (created_at);


--
-- Name: feed_feed_5fc73231; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_feed_5fc73231 ON feed_feed USING btree (date);


--
-- Name: feed_feed_9afea17b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_feed_9afea17b ON feed_feed USING btree (instrument_id);


--
-- Name: feed_feed_afd1a1a8; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_feed_afd1a1a8 ON feed_feed USING btree (updated_at);


--
-- Name: feed_feed_fad6c43b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_feed_fad6c43b ON feed_feed USING btree (frequency);


--
-- Name: feed_feed_fde81f11; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_feed_fde81f11 ON feed_feed USING btree (created_at);


--
-- Name: feed_instrument_0f9f2d92; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_0f9f2d92 ON feed_instrument USING btree (mult);


--
-- Name: feed_instrument_193240a0; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_193240a0 ON feed_instrument USING btree ("secType");


--
-- Name: feed_instrument_1db70381; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_1db70381 ON feed_instrument USING btree ("liquidHours");


--
-- Name: feed_instrument_229543a1; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_229543a1 ON feed_instrument USING btree (local_sym);


--
-- Name: feed_instrument_3bfd35b6; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_3bfd35b6 ON feed_instrument USING btree ("tradingHours");


--
-- Name: feed_instrument_3ca59627; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_3ca59627 ON feed_instrument USING btree (trade_freq);


--
-- Name: feed_instrument_4546e386; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_4546e386 ON feed_instrument USING btree ("evRule");


--
-- Name: feed_instrument_601c7ddc; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_601c7ddc ON feed_instrument USING btree (expiry);


--
-- Name: feed_instrument_871489d5; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_871489d5 ON feed_instrument USING btree (exch);


--
-- Name: feed_instrument_9842a082; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_9842a082 ON feed_instrument USING btree ("timeZoneId");


--
-- Name: feed_instrument_9eb38def; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_9eb38def ON feed_instrument USING btree ("longName");


--
-- Name: feed_instrument_afd1a1a8; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_afd1a1a8 ON feed_instrument USING btree (updated_at);


--
-- Name: feed_instrument_b5fddf1e; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_b5fddf1e ON feed_instrument USING btree (cur);


--
-- Name: feed_instrument_broker_a3126310_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_broker_a3126310_like ON feed_instrument USING btree (broker varchar_pattern_ops);


--
-- Name: feed_instrument_cce85e72; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_cce85e72 ON feed_instrument USING btree (sym);


--
-- Name: feed_instrument_contractMonth_8520fb1f_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX "feed_instrument_contractMonth_8520fb1f_like" ON feed_instrument USING btree ("contractMonth" varchar_pattern_ops);


--
-- Name: feed_instrument_cur_b83f2b7d_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_cur_b83f2b7d_like ON feed_instrument USING btree (cur varchar_pattern_ops);


--
-- Name: feed_instrument_d8fae1fe; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_d8fae1fe ON feed_instrument USING btree ("underConId");


--
-- Name: feed_instrument_e2f3ef5b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_e2f3ef5b ON feed_instrument USING btree (resource_id);


--
-- Name: feed_instrument_e3c9c373; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_e3c9c373 ON feed_instrument USING btree (broker);


--
-- Name: feed_instrument_e69952b0; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_e69952b0 ON feed_instrument USING btree ("minTick");


--
-- Name: feed_instrument_ea6e7a9b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_ea6e7a9b ON feed_instrument USING btree ("contractMonth");


--
-- Name: feed_instrument_evRule_552cf5d9_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX "feed_instrument_evRule_552cf5d9_like" ON feed_instrument USING btree ("evRule" varchar_pattern_ops);


--
-- Name: feed_instrument_exch_77721e7e_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_exch_77721e7e_like ON feed_instrument USING btree (exch varchar_pattern_ops);


--
-- Name: feed_instrument_expiry_504c67ae_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_expiry_504c67ae_like ON feed_instrument USING btree (expiry varchar_pattern_ops);


--
-- Name: feed_instrument_fde81f11; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_fde81f11 ON feed_instrument USING btree (created_at);


--
-- Name: feed_instrument_liquidHours_20e8e776_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX "feed_instrument_liquidHours_20e8e776_like" ON feed_instrument USING btree ("liquidHours" varchar_pattern_ops);


--
-- Name: feed_instrument_local_sym_1aca0177_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_local_sym_1aca0177_like ON feed_instrument USING btree (local_sym varchar_pattern_ops);


--
-- Name: feed_instrument_longName_e34e500b_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX "feed_instrument_longName_e34e500b_like" ON feed_instrument USING btree ("longName" varchar_pattern_ops);


--
-- Name: feed_instrument_secType_de52e714_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX "feed_instrument_secType_de52e714_like" ON feed_instrument USING btree ("secType" varchar_pattern_ops);


--
-- Name: feed_instrument_sym_d46eb656_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_instrument_sym_d46eb656_like ON feed_instrument USING btree (sym varchar_pattern_ops);


--
-- Name: feed_instrument_timeZoneId_8dd635fa_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX "feed_instrument_timeZoneId_8dd635fa_like" ON feed_instrument USING btree ("timeZoneId" varchar_pattern_ops);


--
-- Name: feed_instrument_tradingHours_7cba5ab7_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX "feed_instrument_tradingHours_7cba5ab7_like" ON feed_instrument USING btree ("tradingHours" varchar_pattern_ops);


--
-- Name: feed_prediction_5fc73231; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_prediction_5fc73231 ON feed_prediction USING btree (date);


--
-- Name: feed_prediction_9afea17b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_prediction_9afea17b ON feed_prediction USING btree (instrument_id);


--
-- Name: feed_prediction_afd1a1a8; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_prediction_afd1a1a8 ON feed_prediction USING btree (updated_at);


--
-- Name: feed_prediction_d7a744c6; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_prediction_d7a744c6 ON feed_prediction USING btree (pred_start_date);


--
-- Name: feed_prediction_fad6c43b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_prediction_fad6c43b ON feed_prediction USING btree (frequency);


--
-- Name: feed_prediction_fde81f11; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_prediction_fde81f11 ON feed_prediction USING btree (created_at);


--
-- Name: feed_resource_11725655; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_11725655 ON feed_resource USING btree (is_public);


--
-- Name: feed_resource_154c1303; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_154c1303 ON feed_resource USING btree (sec_cik);


--
-- Name: feed_resource_22b6a063; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_22b6a063 ON feed_resource USING btree (sec_cik_int);


--
-- Name: feed_resource_4264c638; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_4264c638 ON feed_resource USING btree (is_active);


--
-- Name: feed_resource_4562f0d0; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_4562f0d0 ON feed_resource USING btree (resource_type);


--
-- Name: feed_resource_5c731c8c; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_5c731c8c ON feed_resource USING btree (exchange);


--
-- Name: feed_resource_8a084cf7; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_8a084cf7 ON feed_resource USING btree (ticker);


--
-- Name: feed_resource_a9b0c97b; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_a9b0c97b ON feed_resource USING btree (last_edited_time);


--
-- Name: feed_resource_bb5855f0; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_bb5855f0 ON feed_resource USING btree (created_time);


--
-- Name: feed_resource_c1007e8a; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_c1007e8a ON feed_resource USING btree (company_name);


--
-- Name: feed_resource_commodity_type_bc197f94_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_commodity_type_bc197f94_like ON feed_resource USING btree (commodity_type varchar_pattern_ops);


--
-- Name: feed_resource_company_name_abef8a5e_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_company_name_abef8a5e_like ON feed_resource USING btree (company_name varchar_pattern_ops);


--
-- Name: feed_resource_d983bbbb; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_d983bbbb ON feed_resource USING btree (commodity_type);


--
-- Name: feed_resource_exchange_03275740_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_exchange_03275740_like ON feed_resource USING btree (exchange varchar_pattern_ops);


--
-- Name: feed_resource_resource_type_c217f736_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_resource_type_c217f736_like ON feed_resource USING btree (resource_type varchar_pattern_ops);


--
-- Name: feed_resource_sec_cik_5af9202b_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_sec_cik_5af9202b_like ON feed_resource USING btree (sec_cik varchar_pattern_ops);


--
-- Name: feed_resource_sec_cik_int_7a76d387_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_sec_cik_int_7a76d387_like ON feed_resource USING btree (sec_cik_int varchar_pattern_ops);


--
-- Name: feed_resource_ticker_1a790a4b_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_resource_ticker_1a790a4b_like ON feed_resource USING btree (ticker varchar_pattern_ops);


--
-- Name: feed_system_1267705f; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_1267705f ON feed_system USING btree (c2mult);


--
-- Name: feed_system_2af72f10; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_2af72f10 ON feed_system USING btree (version);


--
-- Name: feed_system_3ca59627; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_3ca59627 ON feed_system USING btree (trade_freq);


--
-- Name: feed_system_48b578af; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_48b578af ON feed_system USING btree (ibmult);


--
-- Name: feed_system_521345a9; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_521345a9 ON feed_system USING btree (signal);


--
-- Name: feed_system_54b53072; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_54b53072 ON feed_system USING btree (system);


--
-- Name: feed_system_5ece3b5a; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_5ece3b5a ON feed_system USING btree (c2qty);


--
-- Name: feed_system_5fa7c197; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_5fa7c197 ON feed_system USING btree (c2instrument_id);


--
-- Name: feed_system_6596891a; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_6596891a ON feed_system USING btree (c2api);


--
-- Name: feed_system_72701e21; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_72701e21 ON feed_system USING btree (c2id);


--
-- Name: feed_system_73875049; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_73875049 ON feed_system USING btree (ibqty);


--
-- Name: feed_system_b068931c; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_b068931c ON feed_system USING btree (name);


--
-- Name: feed_system_bbff59fd; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_bbff59fd ON feed_system USING btree (ibinstrument_id);


--
-- Name: feed_system_c2api_b3e8c21b_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_c2api_b3e8c21b_like ON feed_system USING btree (c2api varchar_pattern_ops);


--
-- Name: feed_system_c2id_07240d8c_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_c2id_07240d8c_like ON feed_system USING btree (c2id varchar_pattern_ops);


--
-- Name: feed_system_name_9c91e47f_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_name_9c91e47f_like ON feed_system USING btree (name varchar_pattern_ops);


--
-- Name: feed_system_signal_e8d4abb4_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_signal_e8d4abb4_like ON feed_system USING btree (signal varchar_pattern_ops);


--
-- Name: feed_system_system_61d23838_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_system_61d23838_like ON feed_system USING btree (system varchar_pattern_ops);


--
-- Name: feed_system_version_f22c70e5_like; Type: INDEX; Schema: public; Owner: tsdp
--

CREATE INDEX feed_system_version_f22c70e5_like ON feed_system USING btree (version varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: tsdp
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

