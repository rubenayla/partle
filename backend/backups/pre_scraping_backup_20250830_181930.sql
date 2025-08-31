--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.9 (Ubuntu 16.9-0ubuntu0.24.04.1)

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

--
-- Name: store_type; Type: TYPE; Schema: public; Owner: partle_user
--

CREATE TYPE public.store_type AS ENUM (
    'physical',
    'online',
    'chain'
);


ALTER TYPE public.store_type OWNER TO partle_user;

--
-- Name: store_type_old; Type: TYPE; Schema: public; Owner: partle_user
--

CREATE TYPE public.store_type_old AS ENUM (
    'physical',
    'online',
    'chain'
);


ALTER TYPE public.store_type_old OWNER TO partle_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO partle_user;

--
-- Name: credentials; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.credentials (
    id integer NOT NULL,
    credential_id bytea NOT NULL,
    public_key bytea NOT NULL,
    sign_count integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.credentials OWNER TO partle_user;

--
-- Name: credentials_id_seq; Type: SEQUENCE; Schema: public; Owner: partle_user
--

CREATE SEQUENCE public.credentials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.credentials_id_seq OWNER TO partle_user;

--
-- Name: credentials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: partle_user
--

ALTER SEQUENCE public.credentials_id_seq OWNED BY public.credentials.id;


--
-- Name: product_tags; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.product_tags (
    product_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.product_tags OWNER TO partle_user;

--
-- Name: products; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying NOT NULL,
    spec character varying,
    price numeric(10,2),
    url character varying,
    lat double precision,
    lon double precision,
    description text,
    store_id integer,
    creator_id integer,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_by_id integer,
    image_url character varying,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.products OWNER TO partle_user;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: partle_user
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO partle_user;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: partle_user
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: store_tags; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.store_tags (
    store_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.store_tags OWNER TO partle_user;

--
-- Name: stores; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.stores (
    id integer NOT NULL,
    name character varying NOT NULL,
    type public.store_type NOT NULL,
    lat double precision,
    lon double precision,
    address character varying,
    homepage character varying,
    owner_id integer
);


ALTER TABLE public.stores OWNER TO partle_user;

--
-- Name: stores_id_seq; Type: SEQUENCE; Schema: public; Owner: partle_user
--

CREATE SEQUENCE public.stores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stores_id_seq OWNER TO partle_user;

--
-- Name: stores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: partle_user
--

ALTER SEQUENCE public.stores_id_seq OWNED BY public.stores.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.tags OWNER TO partle_user;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: partle_user
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO partle_user;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: partle_user
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: user_tags; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.user_tags (
    user_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.user_tags OWNER TO partle_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: partle_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    password_hash character varying
);


ALTER TABLE public.users OWNER TO partle_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: partle_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO partle_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: partle_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: credentials id; Type: DEFAULT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.credentials ALTER COLUMN id SET DEFAULT nextval('public.credentials_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: stores id; Type: DEFAULT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.stores ALTER COLUMN id SET DEFAULT nextval('public.stores_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.alembic_version (version_num) FROM stdin;
ad27e536d3af
\.


--
-- Data for Name: credentials; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.credentials (id, credential_id, public_key, sign_count, user_id) FROM stdin;
\.


--
-- Data for Name: product_tags; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.product_tags (product_id, tag_id) FROM stdin;
22	1
13	1
2	1
23	1
14	1
3	1
24	1
4	1
15	1
25	1
5	1
16	1
26	1
6	1
17	1
27	1
7	1
18	1
28	1
8	1
19	1
29	1
9	1
20	1
30	1
10	1
31	1
21	1
11	1
12	1
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.products (id, name, spec, price, url, lat, lon, description, store_id, creator_id, updated_at, updated_by_id, image_url, created_at) FROM stdin;
1	JST-PH 2-pin	\N	0.12	\N	\N	\N	\N	1	1	2025-07-28 21:46:04.161425+00	\N	\N	2025-07-26 21:46:04.163067+00
33	c	\N	\N	\N	\N	\N	c	\N	11	2025-07-30 09:57:15.347566+00	11	\N	2025-07-30 09:57:15.347566+00
36	test2	\N	\N	\N	\N	\N	test2	\N	11	2025-07-30 22:25:11.61831+00	11	\N	2025-07-30 22:25:11.61831+00
38	test3	\N	\N	\N	\N	\N	test3	\N	11	2025-07-30 22:42:52.626149+00	11	\N	2025-07-30 22:42:52.626149+00
2	Essence Mascara Lash Princess	\N	9.99	\N	\N	\N	The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/353/234	2025-07-26 23:18:58.356615+00
3	Eyeshadow Palette with Mirror	\N	19.99	\N	\N	\N	The Eyeshadow Palette with Mirror offers a versatile range of eyeshadow shades for creating stunning eye looks. With a built-in mirror, it's convenient for on-the-go makeup application.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/201/234	2025-07-27 00:51:52.550163+00
4	Powder Canister	\N	14.99	\N	\N	\N	The Powder Canister is a finely milled setting powder designed to set makeup and control shine. With a lightweight and translucent formula, it provides a smooth and matte finish.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/370/308	2025-07-27 02:24:46.743711+00
5	Red Lipstick	\N	12.99	\N	\N	\N	The Red Lipstick is a classic and bold choice for adding a pop of color to your lips. With a creamy and pigmented formula, it provides a vibrant and long-lasting finish.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/274/342	2025-07-27 03:57:40.937259+00
6	Red Nail Polish	\N	8.99	\N	\N	\N	The Red Nail Polish offers a rich and glossy red hue for vibrant and polished nails. With a quick-drying formula, it provides a salon-quality finish at home.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/282/358	2025-07-27 05:30:35.130807+00
7	Calvin Klein CK One	\N	49.99	\N	\N	\N	CK One by Calvin Klein is a classic unisex fragrance, known for its fresh and clean scent. It's a versatile fragrance suitable for everyday wear.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/282/346	2025-07-27 07:03:29.324355+00
8	Chanel Coco Noir Eau De	\N	129.99	\N	\N	\N	Coco Noir by Chanel is an elegant and mysterious fragrance, featuring notes of grapefruit, rose, and sandalwood. Perfect for evening occasions.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/225/346	2025-07-27 08:36:23.517903+00
9	Dior J'adore	\N	89.99	\N	\N	\N	J'adore by Dior is a luxurious and floral fragrance, known for its blend of ylang-ylang, rose, and jasmine. It embodies femininity and sophistication.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/265/238	2025-07-27 10:09:17.711451+00
34	test1	\N	\N	\N	\N	\N	test1	\N	11	2025-07-30 10:23:26.189407+00	11	\N	2025-07-30 10:23:26.189407+00
10	Dolce Shine Eau de	\N	69.99	\N	\N	\N	Dolce Shine by Dolce & Gabbana is a vibrant and fruity fragrance, featuring notes of mango, jasmine, and blonde woods. It's a joyful and youthful scent.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/374/390	2025-07-27 11:42:11.904999+00
11	Gucci Bloom Eau de	\N	79.99	\N	\N	\N	Gucci Bloom by Gucci is a floral and captivating fragrance, with notes of tuberose, jasmine, and Rangoon creeper. It's a modern and romantic scent.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/306/332	2025-07-27 13:15:06.098547+00
12	Annibale Colombo Bed	\N	1899.99	\N	\N	\N	The Annibale Colombo Bed is a luxurious and elegant bed frame, crafted with high-quality materials for a comfortable and stylish bedroom.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/328/337	2025-07-27 14:48:00.292095+00
13	Annibale Colombo Sofa	\N	2499.99	\N	\N	\N	The Annibale Colombo Sofa is a sophisticated and comfortable seating option, featuring exquisite design and premium upholstery for your living room.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/231/226	2025-07-27 16:20:54.485643+00
14	Bedside Table African Cherry	\N	299.99	\N	\N	\N	The Bedside Table in African Cherry is a stylish and functional addition to your bedroom, providing convenient storage space and a touch of elegance.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/317/288	2025-07-27 17:53:48.679191+00
15	Knoll Saarinen Executive Conference Chair	\N	499.99	\N	\N	\N	The Knoll Saarinen Executive Conference Chair is a modern and ergonomic chair, perfect for your office or conference room with its timeless design.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/303/246	2025-07-27 19:26:42.872739+00
16	Wooden Bathroom Sink With Mirror	\N	799.99	\N	\N	\N	The Wooden Bathroom Sink with Mirror is a unique and stylish addition to your bathroom, featuring a wooden sink countertop and a matching mirror.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/257/325	2025-07-27 20:59:37.066287+00
17	Apple	\N	1.99	\N	\N	\N	Fresh and crisp apples, perfect for snacking or incorporating into various recipes.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/393/378	2025-07-27 22:32:31.259835+00
18	Beef Steak	\N	12.99	\N	\N	\N	High-quality beef steak, great for grilling or cooking to your preferred level of doneness.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/328/256	2025-07-28 00:05:25.453383+00
19	Cat Food	\N	8.99	\N	\N	\N	Nutritious cat food formulated to meet the dietary needs of your feline friend.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/262/398	2025-07-28 01:38:19.646931+00
20	Chicken Meat	\N	9.99	\N	\N	\N	Fresh and tender chicken meat, suitable for various culinary preparations.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/377/258	2025-07-28 03:11:13.840479+00
21	Cooking Oil	\N	4.99	\N	\N	\N	Versatile cooking oil suitable for frying, sautéing, and various culinary applications.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/395/331	2025-07-28 04:44:08.034027+00
22	Cucumber	\N	1.49	\N	\N	\N	Crisp and hydrating cucumbers, ideal for salads, snacks, or as a refreshing side.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/386/227	2025-07-28 06:17:02.227575+00
23	Dog Food	\N	10.99	\N	\N	\N	Specially formulated dog food designed to provide essential nutrients for your canine companion.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/301/352	2025-07-28 07:49:56.421123+00
24	Eggs	\N	2.99	\N	\N	\N	Fresh eggs, a versatile ingredient for baking, cooking, or breakfast.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/205/306	2025-07-28 09:22:50.614671+00
25	Fish Steak	\N	14.99	\N	\N	\N	Quality fish steak, suitable for grilling, baking, or pan-searing.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/369/258	2025-07-28 10:55:44.808219+00
26	Green Bell Pepper	\N	1.29	\N	\N	\N	Fresh and vibrant green bell pepper, perfect for adding color and flavor to your dishes.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/236/206	2025-07-28 12:28:39.001767+00
27	Green Chili Pepper	\N	0.99	\N	\N	\N	Spicy green chili pepper, ideal for adding heat to your favorite recipes.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/386/283	2025-07-28 14:01:33.195315+00
35	Nothing	\N	\N	\N	\N	\N	Nothing	\N	11	2025-07-30 22:09:21.329298+00	11	\N	2025-07-30 22:09:21.329298+00
28	Honey Jar	\N	6.99	\N	\N	\N	Pure and natural honey in a convenient jar, perfect for sweetening beverages or drizzling over food.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/269/331	2025-07-28 15:34:27.388863+00
29	Ice Cream	\N	5.49	\N	\N	\N	Creamy and delicious ice cream, available in various flavors for a delightful treat.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/386/344	2025-07-28 17:07:21.582411+00
30	Juice	\N	3.99	\N	\N	\N	Refreshing fruit juice, packed with vitamins and great for staying hydrated.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/324/241	2025-07-28 18:40:15.775959+00
31	Kiwi	\N	2.49	\N	\N	\N	Nutrient-rich kiwi, perfect for snacking or adding a tropical twist to your dishes.	\N	\N	2025-07-29 08:15:48.147272+00	\N	https://picsum.photos/240/333	2025-07-28 20:13:09.969507+00
37	TEST PRODUCT - DELETE ME	\N	99.99	https://test.example.com/test-product	\N	\N	This is a test product created by the scraper test	4064	\N	2025-08-28 15:22:04.920581+00	\N	https://test.example.com/test-image.jpg	2025-07-30 20:33:11.155739+00
\.


--
-- Data for Name: store_tags; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.store_tags (store_id, tag_id) FROM stdin;
\.


--
-- Data for Name: stores; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.stores (id, name, type, lat, lon, address, homepage, owner_id) FROM stdin;
2	kkstore	physical	0	0	kkstreet	\N	10
3	pppp	physical	0	0	pppp	\N	10
4	test	physical	0	0		\N	11
1	Electro Depot Almería	physical	36.8401	-2.4598	C/ Sierra Nevada 123	https://electro-depot.es/almeria	\N
6	Ferretería JA	physical	40.4860185	-3.6901201	\N	\N	12
7	Ferretería de Aluminio Carmetal	physical	40.4870215	-3.6890489	\N	\N	12
8	Leroy Merlin	physical	38.3704654	-0.4680452	\N	\N	12
9	ferretería Brico-Lloret	physical	38.3666636	-0.4287264	\N	\N	12
10	Produmarsan Suministros Industriales	physical	37.3545844	-2.2942087	\N	\N	12
11	Comercial Ferrosan	physical	36.8313225	-2.4491202	Avenida de Madrid, 3, 04007, Almería	\N	12
12	Cerrajería Pelayos	physical	40.3612619	-4.3279435	\N	\N	12
13	Servei Estació	physical	41.3915276	2.1643195	Carrer d'Aragó, 272, 08007	https://serveiestacio.com/	12
14	La Barata	physical	43.3521238	-3.7046525	Avenida de Alisas, 35, 39720, La Cavada	\N	12
15	Ferreteria i Loteria Poma	physical	41.63809	2.2323742	\N	\N	12
16	Ferretería Hermanos Marco	physical	38.2745331	-0.5386934	avinguda de Cartagena, 38, Elche	\N	12
17	Ferretería Alonso	physical	43.0534973	-2.1807032	\N	\N	12
18	Alonso	physical	43.0534944	-2.1808836	\N	\N	12
19	Centro Comercial del bricolaje	physical	41.7681188	-2.4858903	\N	\N	12
20	Ikelatz	physical	43.3099269	-2.0066484	\N	\N	12
21	Marcos Decoración	physical	43.3032188	-1.978974	\N	\N	12
22	PC BOX	physical	39.4764525	-0.3618108	\N	\N	12
23	Persianas Gradulux	physical	28.1160436	-15.4222253	\N	\N	12
24	Usansolo Gorosibi	physical	43.2185308	-2.8146781	\N	\N	12
25	NOVACERO S.A.L.	physical	42.836789	-2.7354269	\N	\N	12
26	Brico House	physical	37.9449791	-0.7169182	\N	\N	12
27	BriCor	physical	42.2323399	-8.7180137	\N	\N	12
28	Ferreteria Molina	physical	36.7487872	-4.0620649	\N	\N	12
29	Comercial Raybe	physical	43.389065	-3.6906594	\N	\N	12
30	Ferretería	physical	38.3912295	-0.5060292	\N	\N	12
31	Charanga Ume erropak	physical	43.0303271	-2.4106561	\N	\N	12
32	Udana Barne Diseinua	physical	43.0314752	-2.4145185	\N	\N	12
33	Elorza	physical	43.0322832	-2.4122135	\N	\N	12
34	Beloki Iturgintza	physical	43.0334818	-2.4121049	\N	\N	12
35	Laket2 Konplementoak	physical	43.0309972	-2.4135942	\N	\N	12
36	Lantzen	physical	43.0313845	-2.4100378	\N	\N	12
37	Quelle Sastrea	physical	43.0317631	-2.4117782	\N	\N	12
38	Begoña Apaindegia	physical	43.0320079	-2.4125986	\N	\N	12
39	BAIO Jantziak	physical	43.0318969	-2.4120016	\N	\N	12
40	d'or Apaindegia	physical	43.0303369	-2.4128443	\N	\N	12
41	Lentzeria	physical	43.0304303	-2.4125074	\N	\N	12
42	La Llave	physical	41.7633296	-2.4691381	\N	\N	12
43	Habitacle	physical	40.356459	-4.3425327	\N	\N	12
44	Landetxe	physical	43.3281675	-1.8246049	Gabiria, 3, 20305, Irun	\N	12
45	Ferreteria Cima	physical	28.1845449	-14.1521923	\N	\N	12
46	Elkar, Calibrados	physical	43.1727825	-2.4114924	Santa Ana kalea, 30, 20590, Soraluze - Placencia de Las Armas	\N	12
47	Tornilleria	physical	43.1722881	-2.4099101	Santa Ana kalea, 40, 20590, Soraluze - Placencia de Las Armas	\N	12
48	Arantxa	physical	43.0326186	-2.4045166	\N	\N	12
49	Arpun - 1	physical	41.4418336	2.2190764	Ronda de Sant Antoni de Llefià, Badalona	\N	12
50	Miele	physical	38.3632175	-0.4678684	\N	\N	12
51	Ferretería 3 llaves	physical	38.3873508	-0.4111038	\N	\N	12
52	Beca-Medri	physical	41.3844697	2.1684824	\N	\N	12
53	Arigara	physical	43.066264	-2.480478	\N	\N	12
54	Almacén de tableros Antolin	physical	38.3758602	-0.4995464	\N	\N	12
55	Piscijardín Rico	physical	40.3576039	-4.3421816	\N	\N	12
56	Ferretería Perez hnos.	physical	42.4659943	-2.4566831	\N	\N	12
57	Sapi sapi	physical	42.4659805	-2.4566187	\N	\N	12
58	Ferretería Cancho	physical	39.4674357	-6.3800615	Avenida de Alemania, 8, 10001, Cáceres	\N	12
59	Ferretería Autoferr	physical	39.4717306	-6.3930284	Calle Monfragüe, 7B, 10005, Cáceres	\N	12
60	Ferretería Diosán	physical	39.4692993	-6.3780108	Calle Profesor Rodríguez Moñino, 2, 10001, Cáceres	\N	12
61	Ferretería Cancho_1	physical	39.4593764	-6.3727339	Calle Colombia, 6, 10005, Cáceres	\N	12
62	Suministros Aguado	physical	43.2808876	-2.0115977	Fernando Mugica kalea, 10, 20018, Donostia / San Sebastián	https://www.suministrosaguado.com/	12
63	Ferreteria Noemí	physical	40.5418663	0.482736	\N	\N	12
64	Leroy Merlin_1	physical	38.0381689	-1.1517418	\N	\N	12
65	Pinturas Nacional	physical	42.4654369	-2.454677	\N	\N	12
66	Pinturas Procolor	physical	42.4659239	-2.4564221	\N	\N	12
67	Barredo	physical	42.8509067	-2.684454	\N	\N	12
68	Ferreteria Vilassar	physical	41.504309	2.3934307	\N	\N	12
69	Pintor Romeu	physical	41.5012623	2.3853185	\N	\N	12
70	Cristalleria	physical	41.5046885	2.3964412	\N	\N	12
71	Hermanos García	physical	39.5445591	-0.5604912	\N	\N	12
72	Ferretería FerrCash	physical	40.457982	-3.4532427	\N	\N	12
73	Saneamientos Los Chicos	physical	40.4581673	-3.4710061	Calle de Roma, 3	https://www.fontanerialoschicos.com/	12
74	Ferretería Comercial Vialpa	physical	28.762221	-17.9787668	\N	\N	12
75	Ferreria Ca'n Guillem Costa	physical	39.6496094	3.1132374	\N	\N	12
76	Depuradores Álvarez	physical	39.5647103	-0.5310119	\N	\N	12
77	Krisval	physical	39.5640995	-0.5313745	\N	\N	12
78	Ferretería Ábaco Suytec, s.a.u.	physical	40.4521746	-3.4639786	\N	https://www.abacosuytec.com/	12
79	Lorente	physical	37.8294536	-1.1580469	\N	\N	12
80	Javier Clemente	physical	37.8313661	-1.1555444	\N	\N	12
81	Manualidades Mariví	physical	42.0027099	-5.6805483	\N	\N	12
82	Bar Tapaboca	physical	36.0121354	-5.6026902	Calle Guzmán el Bueno, 9, 11380	\N	12
83	Casa Gregorio	physical	42.1918503	0.3382983	\N	\N	12
84	Aluminios Vicent	physical	38.5121769	-0.2205807	\N	\N	12
85	Ferretería La Merced	physical	37.2627482	-6.9529181	Paseo de la Independencia, 33, 21002, Huelva	\N	12
86	Ferretería López	physical	28.4877678	-16.3164959	\N	\N	12
87	Ferretería Ceboleiro	physical	42.7876582	-8.8885592	\N	\N	12
88	Ferrodeco	physical	40.1169275	-0.0497154	\N	\N	12
89	Brico Leal	physical	42.3036257	-3.701991	\N	\N	12
90	Brico Centro	physical	42.3550238	-3.6607755	\N	\N	12
91	Can Reig	physical	41.6825497	2.2860355	\N	\N	12
92	Merino	physical	41.3770044	2.1698129	\N	\N	12
93	A Fonte	physical	43.2650691	-8.9630194	\N	\N	12
94	Brico Cento López Fernández	physical	37.1286842	-1.8320584	Paseo del Mediterráneo, 317, 04638, Mojácar Playa	https://lopezferreteria.es/	12
95	Bricojardin	physical	36.7469144	-3.8806903	\N	http://www.ferreteriabricojardin.com	12
97	Planícia	physical	39.6710496	2.5061092	\N	\N	12
98	Pla4	physical	38.7633694	0.1904751	\N	\N	12
99	Jerez	physical	37.8446589	-3.0669071	\N	\N	12
100	Ferretería Ángel	physical	37.8437528	-3.0669261	\N	\N	12
101	La Chispa	physical	39.4536867	-0.3896574	\N	\N	12
102	Moraluminio	physical	39.4539214	-0.3902407	\N	\N	12
103	Mercería-Droguería-Ferretería-Regalos Bazar Andalucía	physical	37.9943894	-3.4655823	\N	\N	12
104	Cerrajería Rubén Darío 2	physical	37.982662	-1.1272419	\N	\N	12
105	Taller Mecánico Mobylette Derby	physical	37.9947978	-3.4646468	\N	\N	12
106	Leroy Merlin Compact	physical	43.0381503	-7.569931	\N	\N	12
107	La Reserva	physical	36.742422	-2.6183027	\N	\N	12
108	Almacen de ferreteria industrial	physical	38.0033594	-3.4728081	\N	\N	12
114	Yeste	physical	38.3672382	-2.3186772	\N	\N	12
115	Ferretería Juangalo	physical	37.7581964	-0.8393551	\N	\N	12
116	Casa Dominga	physical	36.6172301	-5.3418859	\N	\N	12
117	Construcciones y Contratas Martin e Hijos	physical	37.9931783	-3.4651324	23440, Baeza	\N	12
118	Toldos Sánchez	physical	37.9940501	-3.4634689	\N	\N	12
119	Mármoles Videma Garrido y Martínez C.B.	physical	38.0015581	-3.4610582	\N	\N	12
120	Cristalería "Palomares"	physical	37.9981414	-3.4736942	\N	\N	12
121	Maquinaria	physical	37.9989348	-3.4737705	\N	\N	12
122	Material de Construcción "Hogar y cerámica"	physical	37.9992202	-3.4742855	\N	\N	12
123	Carpinteria metálica "Hermanos Soto"	physical	37.9980595	-3.4736489	\N	\N	12
124	Carpinteria metálica "Hermanos Soto"_1	physical	37.9983114	-3.4733293	\N	\N	12
125	Construcciones "Marjisur 2005"	physical	37.9990232	-3.4755473	\N	\N	12
126	Maquinaria "Herrera Montoro"	physical	37.9981225	-3.4745758	\N	\N	12
127	Cristalería "José María Luna"	physical	37.9984103	-3.4753624	\N	\N	12
128	Construcciones "Marjisur 2005"_1	physical	37.9983283	-3.4730651	\N	\N	12
129	Construcciones "Fuentegula"	physical	37.9991712	-3.4755788	\N	\N	12
130	Construcciones "Andrés Cejudo García"	physical	37.9954758	-3.4729178	\N	\N	12
135	Brico Noia	physical	42.7895946	-8.888169	\N	\N	12
136	Ferrateria Alfonso	physical	28.2388685	-16.8405577	\N	\N	12
137	Drogería Norte	physical	43.420218	-4.7570392	\N	\N	12
138	Guanipa	physical	28.3805293	-16.6809223	\N	\N	12
139	C. Aluminio Espinosa de Levante	physical	38.3905944	-0.5145366	\N	\N	12
140	Cofer iluminación S.L.	physical	38.3894955	-0.5118189	\N	\N	12
141	Bueno	physical	38.3936656	-0.5159348	La esperanza, San vicente del raspeig	\N	12
142	Yesos y molduras	physical	38.3945302	-0.5160099	\N	\N	12
143	Ferretería Hoyos	physical	40.4110324	-3.7074309	\N	\N	12
144	Omega Asistencia Tecnica S.L.	physical	43.5402842	-5.6930154	Calle Luis Braille, 27-29, 33212, Gijón/Xixón	http://www.omegasl.es/	12
145	Gravina	physical	39.4175553	3.2571063	\N	\N	12
146	Suministros Asín	physical	42.3383601	-1.8101032	\N	\N	12
147	Ferreteria Yago	physical	41.6322264	-0.7492412	Calle de Eras Altas, 8, 50171	https://www.ferreteriayago.com/	12
153	Tornillos-Online	physical	38.0183226	-0.7661367	Los Perez, 13, 03187	\N	12
190	Ferreteria Diaz	physical	39.1816849	-6.2327154	\N	\N	12
191	Aeromodelismo Speed Hobbys	physical	40.4323582	-3.711801	Calle de Blasco de Garay, 19, 28015, Madrid	http://www.aeromodelismospeedhobbys.com/	12
192	Plásticos	physical	40.4323036	-3.7023659	\N	\N	12
193	Emir Gas SL	physical	40.4491938	-3.4686652	Plaza del Progreso, 2	\N	12
194	Ferretería J. Teo Amate	physical	42.817565	-8.5445196	\N	\N	12
195	Ferretería Caamaño	physical	42.7839188	-8.8892123	\N	\N	12
196	Campo y Hogar	physical	36.4202941	-6.1418679	\N	\N	12
197	La Estación	physical	40.573783	-3.9552977	\N	\N	12
198	Ferretería - Bazar F&R	physical	43.5398819	-7.2386462	\N	\N	12
199	Torres	physical	28.0519137	-14.3507954	\N	\N	12
200	La os Pepes	physical	28.1838362	-14.1523785	\N	\N	12
201	Maselec Valles S.L.	physical	41.5251067	2.1134947	JOSEP COMAS 95, 08204	\N	12
202	HaryFel	physical	27.8058891	-17.9127715	\N	\N	12
203	Fuerteventura	physical	28.5076636	-13.8482352	\N	\N	12
204	Inoxidables Dominguez	physical	28.5038757	-13.8481048	Calle La Pesca, Puerto del Rosario	\N	12
205	Inoxidables Fuerinox	physical	28.505957	-13.8491638	Calle Pelayo	\N	12
206	Tecser Theimer S.L	physical	41.4989678	2.1409284	Carretera de Barcelona, 163, 08290	\N	12
207	apeu arquitectes	physical	39.4736583	-0.343351	\N	\N	12
208	Cuchilleria Sampil	physical	41.67056	-3.6896163	\N	\N	12
209	Serafí	physical	40.88597	0.803042	\N	\N	12
210	Figueres	physical	40.8837669	0.8032568	\N	\N	12
211	Ferreteria Barral	physical	42.1749986	-8.4848575	\N	https://www.ferreteriabarral.es/	12
212	Travis	physical	41.412657	1.9682127	Avinguda Catalunya, 52	\N	12
215	Ancar Caraldiaz	physical	42.2236686	-2.1146263	Avda Numancia, 12, 26580	https://www.eancar.com	12
216	Ferretería Castro Delgado	physical	28.4213391	-16.3202566	\N	\N	12
217	Efraín	physical	42.9324307	-3.4867724	\N	\N	12
218	Fusteria Vicent Alcover	physical	39.557412	-0.3240434	\N	\N	12
219	Quevedo	physical	43.1451223	-1.5178969	Santiago Karrika, 31700, Elizondo	\N	12
224	Ferreteria El martillo	physical	39.4628748	-0.3448991	\N	\N	12
225	Ferreteria Caribe	physical	39.4623968	-0.3435244	\N	\N	12
226	Cuadros Larrayoz	physical	42.8056283	-1.6807216	\N	\N	12
227	Gasteiz	physical	42.8522387	-2.665011	\N	\N	12
228	Bazar Los Cubos	physical	43.0761182	-3.5507262	\N	\N	12
229	Ferretería Rafael Llarena	physical	43.0757461	-3.5499291	Calle del Progreso, 20	\N	12
230	Comercial Pancho	physical	42.3375684	-8.5705035	Alexandre Boveda, 14	\N	12
231	Meno Echevarría	physical	42.8033654	-3.3887142	\N	\N	12
232	Ferretería La Farola	physical	37.1947618	-4.0462618	\N	\N	12
233	Materiais de Construcción Barallobre, s.l.	physical	43.3774824	-8.1636103	90	\N	12
234	Ferretería Edu	physical	37.1974557	-4.0430089	\N	\N	12
235	Breamo	physical	43.3954688	-8.1709698	\N	\N	12
236	Ca'n Vidal	physical	39.6656738	2.5783822	\N	\N	12
237	Agrogarden	physical	38.7759188	0.0822974	\N	\N	12
238	Azulejos Juan	physical	38.774023	0.0856106	\N	\N	12
96	Ferretería Prosperidad	physical	37.3748202	-6.0519749	\N	\N	12
109	Almacenes Tamesa	physical	37.9917358	-3.4733817	\N	\N	12
110	Mundihogar	physical	28.2129816	-14.0194258	\N	\N	12
111	Fali	physical	37.9936923	-3.4691632	Pasaje Cardenal Benavides, 2, 23440, Baeza	\N	12
112	Orgaluz	physical	37.993914	-3.4694643	Calle San Francisco, 23440, Baeza	\N	12
113	Palomarea	physical	37.993581	-3.4688014	Calle San Francisco, 19, 23440, Baeza	\N	12
131	Català	physical	41.2302639	0.5506778	\N	\N	12
132	Correa	physical	43.2358621	-2.8834385	\N	\N	12
133	Leroy Merlin_2	physical	41.6105355	-0.8906721	\N	https://www.leroymerlin.es/	12
134	Saneamientos Fontazul	physical	37.9727735	-1.1358938	\N	\N	12
148	Ferreteria Prince	physical	27.7699624	-15.5846556	Plaza Puerto Del Rosario, 35100	\N	12
149	Aki Zamora Bricolaje	physical	41.5213783	-5.7218157	\N	\N	12
150	FECRA	physical	41.4219285	2.1433495	Carrer d'Arenys, 32, 08035, Barcelona	\N	12
151	Cofac Rubens	physical	41.4278705	2.1585951	\N	\N	12
152	Osvald Ferreteria	physical	41.534153	0.5156528	carrer Lleida, 17, 25170, Torres de Segre	\N	12
154	ATB	physical	42.0836414	-6.6439579	\N	\N	12
155	Curro Telecomunicaciones	physical	36.4287641	-5.1487677	Calle Turia, 29680	https://www.currosat.com/	12
156	Afe Antifuego	physical	36.4287814	-5.1489286	Turia, 29680	https://afe-antifuego.com/	12
157	Ferretería Villamor	physical	40.9673737	-5.6672402	\N	\N	12
158	Pérez Logares	physical	43.4644419	-7.052248	Avda. de Galicia, 33770, Vegadeo	\N	12
159	Urvaca	physical	42.5255532	-1.6735282	\N	\N	12
160	Ferreteria Vega	physical	43.5707029	-7.2583093	\N	\N	12
161	Ferretería Bahía	physical	43.5708008	-7.2579134	\N	\N	12
162	A. Grau	physical	41.5555749	2.0065215	\N	\N	12
163	Urbaca	physical	42.526245	-1.6735379	\N	\N	12
164	Valencia	physical	42.5264106	-1.6744062	\N	\N	12
165	FerroBox	physical	39.4920343	-0.3966796	46015	\N	12
166	Yesos Marcos S.L.	physical	42.5615199	-6.6284352	Avenida de Galicia, 125, 24400, Ponferrada	\N	12
167	Gavi	physical	42.7862032	-8.886398	\N	\N	12
168	Ferreteria	physical	28.0855641	-16.7323601	\N	\N	12
169	Ferretería Arga	physical	42.3390729	-1.8037899	\N	\N	12
170	Arnaveca	physical	42.3956843	-7.1102056	\N	\N	12
171	AutoRepuestos Angel	physical	42.3920692	-7.1186197	Emilia Pardo Bazán, 32350	\N	12
172	Aluminios Dafergu	physical	42.4128384	-7.0568214	\N	\N	12
173	Porcelanosa	physical	38.0291931	-1.1453093	\N	\N	12
174	Ca'n Pou	physical	39.5442559	3.332092	\N	\N	12
175	Fuente el Sol	physical	41.6622784	-4.7336134	\N	\N	12
176	Ferreteria La Clau	physical	41.9950955	1.522304	\N	\N	12
177	Hermanos Sanchez	physical	42.6100648	-7.7697929	\N	\N	12
178	Ferretería Vallecana	physical	40.3780355	-3.6212781	Paseo de Federico García Lorca, 24, 28031, Madrid	\N	12
179	Alberto Adán	physical	40.4555899	-3.462254	\N	\N	12
180	Felipe de Marco	physical	40.45596	-3.4623882	Calle de la Solana, 45	\N	12
181	Ferretería Rodisur	physical	37.7733069	-3.7855042	\N	\N	12
182	Vinuesa	physical	37.1187414	-3.5853237	\N	\N	12
183	Cube La Zubia	physical	37.1160127	-3.5912932	\N	\N	12
184	OPTIMUS Ferreteria Prim	physical	41.4524327	2.2515206	Carrer d'en Prim, 113, 08911, Badalona	https://www.ferreteriaprim.com/ca/	12
185	Bricor	physical	36.6920861	-6.1624295	\N	\N	12
186	Ferretería Sara	physical	37.2921014	-5.9258062	\N	\N	12
187	Ferreteria_1	physical	36.4897599	-4.7151034	\N	\N	12
188	A coser	physical	40.3873189	-3.7590553	\N	\N	12
189	Ferretería Arenal	physical	40.1176112	-3.9304101	\N	\N	12
213	José Días	physical	36.7375871	-3.6839676	\N	\N	12
214	Carbonell	physical	36.7373162	-3.6842627	\N	\N	12
220	Ferretería Los Baldíos	physical	28.4619986	-16.3275494	\N	\N	12
221	Ferretería Ruíz	physical	28.4532281	-16.4475439	\N	\N	12
222	Cristalería Hermanos Cabañas	physical	39.8685405	-3.9550835	\N	\N	12
223	Ferretería El Turpial	physical	43.3267129	-8.3826817	\N	\N	12
249	Metalicas Alberola	physical	38.3925414	-0.5175862	\N	\N	12
250	Ferretería Soterín	physical	38.1327687	-0.6764851	Zona Comercial IV, 126, 03177	\N	12
251	Ferretería Alcaraz	physical	38.1406008	-0.6744372	\N	\N	12
252	Saneamientos Chamorro	physical	40.3784508	-3.7664477	\N	\N	12
253	Silva	physical	42.2237537	-8.7352133	Rúa da Coruña, 52, Vigo	\N	12
254	Beltran	physical	39.9473517	-0.0647835	\N	\N	12
255	Keaki	physical	37.9919165	-0.677591	Avenida Rosa Mazón, 03183, Torrevieja	\N	12
256	Tecnisoft Data & Services	physical	40.4489459	-3.4711694	Calle de Dionisos, 4, 28850	https://www.tecnisoftdata.com/	12
269	FerroBox - La Tienda de Pierre	physical	38.0828139	-0.655632	Carrer Molivent, 14	\N	12
270	Ferretería Arganda (FerroKey)	physical	40.3674938	-3.4876027	Madrid, 1, 28891	\N	12
271	Comercial CID	physical	27.7681245	-15.6081398	\N	\N	12
272	APP	physical	40.5034879	-3.5272688	\N	\N	12
273	Pablos	physical	41.406626	2.1775063	\N	\N	12
274	Ferretería Reina	physical	40.2870193	-3.7937738	\N	\N	12
275	Ferretería Bolaños	physical	40.2861268	-3.7926812	\N	\N	12
285	Mármoles Daniel	physical	38.0019457	-1.1574008	\N	\N	12
297	Ferretería África	physical	38.0280359	-3.1004729	Carretera de Cazorla, 4, 23311, Santo Tomé	\N	12
298	Leroy Merlin_4	physical	37.9294082	-0.7369456	\N	\N	12
299	Ferretería Gíl Cánovas	physical	38.3491598	-0.7642655	\N	\N	12
324	SONJA Casa i Estils	physical	42.1310745	3.1032233	\N	https://www.sonjacasaiestils.com/	12
339	Würth	physical	41.3796837	2.1485533	\N	\N	12
340	Ferretería Montaner	physical	39.4824502	-0.4412464	\N	\N	12
343	Ferretería Arenal_1	physical	40.0846237	-3.8763362	\N	\N	12
344	Sagrera	physical	28.3919143	-16.5180037	Calle Villa de Madrid, 1	https://sagreracanarias.es/	12
345	Fontaneria Garcia	physical	42.5316302	-1.6728832	\N	\N	12
346	Gas Natural	physical	42.5316025	-1.6730065	\N	\N	12
347	Escayolas	physical	42.532407	-1.6718988	\N	\N	12
348	Ferrenorte	physical	28.3940005	-16.5264039	\N	\N	12
349	Mármoles Montornés	physical	41.4514242	2.2336679	\N	\N	12
350	Ferreteria Salas	physical	41.4508891	2.237135	\N	\N	12
428	Zeramikaren benta	physical	43.2915998	-1.5479031	\N	\N	12
453	Ferretería Pascual	physical	42.5512337	-3.3246777	\N	\N	12
454	Bricoleo	physical	38.3441851	-0.7645367	\N	\N	12
455	Lamagrande	physical	38.8783226	-6.9728385	\N	\N	12
574	MR.DIY	physical	42.3526066	-3.6699735	\N	https://www.mrdiy.com/es/	12
239	Ferretería Cañete	physical	38.7750076	0.0840642	\N	\N	12
240	La Patrona	physical	28.2928058	-16.8147675	\N	\N	12
241	Todo Cartucho	physical	42.8475719	-2.6760624	\N	\N	12
242	Gorostidi burdindegia	physical	43.1864936	-2.0531742	\N	\N	12
243	Ferreteria Cal Guillem	physical	42.3696913	1.7773038	\N	\N	12
244	Ceramicas Edel	physical	38.7732048	0.0885214	\N	\N	12
245	L'Ombra Pergoles i Sombralls	physical	38.7739375	0.087131	\N	\N	12
246	Cristalerías Rivas	physical	40.441493	-3.6377333	\N	\N	12
247	Gabriel Fernández	physical	42.9331069	-3.4875141	\N	\N	12
248	Seguí	physical	39.9999961	3.8375273	\N	\N	12
257	Leroy Merlin_3	physical	43.4284465	-3.8401569	\N	\N	12
258	A de Barreiro	physical	42.6994256	-8.6829005	\N	\N	12
259	Alcaraz	physical	38.0299089	-0.7291283	\N	\N	12
260	Aluminios SerraMart	physical	41.4793392	1.9185271	\N	\N	12
261	Subministres Telobis	physical	41.4811553	1.9137255	\N	\N	12
262	Conmasa	physical	41.501655	2.3590878	\N	\N	12
263	Brico Dépôt	physical	41.5185033	2.4182645	\N	\N	12
264	Ferretería Industrial	physical	40.3870247	-3.4832613	\N	\N	12
265	Ferretería Industrial ACIMSA	physical	40.3879472	-3.4887623	Portugal, 3, 28840	\N	12
266	Ferretería y Saneamientos Hidalgo	physical	37.1983738	-4.0490368	\N	\N	12
267	Instalaciones Agrícolas López Martínez J.	physical	37.1975764	-4.0487057	\N	\N	12
268	Sumco	physical	41.2335314	1.7424592	\N	\N	12
276	Ferreteria CIFEC Palafrugell	physical	41.9195699	3.1556437	Carrer del Mestre Sagrera, 31	\N	12
277	Espada Ferreteria	physical	41.9183106	3.1614211	Carrer de Torres Jonama, 42	\N	12
278	Tienda automoción Isana	physical	40.2793047	-3.79987	\N	\N	12
279	Bazar Multipreu	physical	41.723379	2.9322824	\N	\N	12
280	Ferretería Coslada	physical	40.4303825	-3.5380342	Avenida de la Cañada, 40	\N	12
281	Ferretería Muñoz Álvarez	physical	40.2800567	-3.7957144	\N	\N	12
282	Ferretería José Antonio	physical	42.804866	-1.6797936	\N	\N	12
283	Ferretería Aguilón	physical	40.3971558	-3.7014983	Calle Tomás Borrás, 8, 28045, Madrid	\N	12
284	La Ferretería	physical	38.1347387	-0.6874957	\N	\N	12
286	Ferretería La llave	physical	43.1538158	-4.6225667	Calle del Doctor Encinas, 3, 39570	\N	12
287	Gutiérrez-Fernández	physical	43.1542892	-4.6238729	Calle de la Independencia, 18, 39570	\N	12
288	Electric Rafael	physical	42.2454504	3.1261025	Avinguda de Carles Fages de Climent, 6, 17487	\N	12
289	Cristalería Pulido Salamanca	physical	40.2848819	-3.7951627	\N	\N	12
290	Aluminios y Cristales Villalba	physical	40.2870397	-3.7947589	\N	\N	12
291	Ferretería Grupo Hormigo	physical	40.2868488	-3.7970729	\N	\N	12
292	Can Manxa	physical	42.1157409	2.7669138	\N	\N	12
293	Luis Hernández Álvarez, S.L.	physical	42.2635534	-8.7849554	Rúa Real, 1, 36940, Cangas	http://www.luishernandez.es/	12
294	Ferrgenal	physical	36.5195634	-5.3209423	\N	\N	12
295	Comercial Ramón	physical	42.8017686	-5.6301161	\N	\N	12
296	Repuestos Ramírez	physical	40.2882036	-3.7926294	\N	\N	12
300	M Saiz Plásticos	physical	40.4325372	-3.7024214	Calle del Cardenal Cisneros, 47, 28010, Madrid	http://www.plasticosmanuelsaiz.com/	12
301	Ferreteria Las Torres	physical	39.8678462	-3.9442068	\N	\N	12
302	Ferreteria Diagonal	physical	41.3995841	2.1658976	Carrer del Rosselló, 290, 08009, Barcelona	\N	12
303	Soto	physical	38.1097645	-0.7915002	Plaza de la Constitución, 23, 03160	\N	12
304	Cuchillería J. Manuel Veras	physical	41.6459274	-0.8724437	Avenida de San José, 2-4, 50002	\N	12
305	Ferriplus	physical	40.4251432	-3.5371983	\N	\N	12
306	Taller Prieto	physical	41.4455084	-5.7345064	\N	\N	12
307	Puertas Arias	physical	41.4454119	-5.7343723	\N	\N	12
308	Climatizaciones Climateg	physical	41.446005	-5.7319556	\N	\N	12
309	Aluminios Rivetal	physical	41.4444046	-5.7311456	\N	\N	12
310	Laly y Sara	physical	41.4445815	-5.7311429	\N	\N	12
311	Aluminios Cortizo	physical	41.4665815	-5.7370464	\N	\N	12
312	Aspiraciones Zamoranas	physical	41.4657534	-5.7358019	\N	\N	12
313	Agrijar (Jardinería, piscinas...)	physical	41.4466303	-5.7353352	\N	\N	12
314	Almacén Domingo	physical	41.4443061	-5.7311483	\N	\N	12
315	Almacén Domingo_1	physical	41.4491936	-5.72834	\N	\N	12
316	Teka Sevilla	physical	37.4040246	-5.9758026	Santa Maria de la Hiedra, 1 lc2, 41008, Sevilla	https://www.tekasevilla.es/	12
317	Rayanico	physical	42.083606	-6.6431541	\N	\N	12
318	Calvo y Munar	physical	40.4539969	-3.4945797	\N	\N	12
319	DIY	physical	42.9342983	-3.4858014	\N	\N	12
320	Fontanería Calero	physical	42.0856621	-6.641083	\N	\N	12
321	Automòbils Sabata	physical	42.137533	1.5904869	\N	\N	12
322	Ferretería Penalva	physical	38.087072	-0.720839	Calle de Zulaida, 24	\N	12
323	Comercial Galindo	physical	38.538428	-0.1083868	\N	\N	12
325	Nolasco	physical	28.6348233	-17.7701756	\N	\N	12
326	Fontanería Cobreplas	physical	37.3896043	-5.9703975	\N	\N	12
327	Ferretería Rufo	physical	40.3702241	-3.708581	Calle Gran Avenida, 17 posterior, 28041	\N	12
328	Casa Romero	physical	42.0260536	-3.7601662	\N	\N	12
329	Chimborazo	physical	28.4150378	-16.5486471	\N	\N	12
330	La Arena	physical	28.2271951	-16.839687	\N	\N	12
331	Instal·lacions Elèctriques CAT, S.A.U.	physical	41.7448345	2.6277191	Poeta Ruyra, 5, 17450, Hostalric	https://www.iecat.es/	12
332	Ferretería Melo	physical	42.9389149	-3.5724484	Plaza Mayor, 16	\N	12
333	Ferretería Roberto	physical	43.3849958	-5.7029522	\N	\N	12
334	Ferretería Álvarez Nava	physical	43.3849199	-5.7034671	\N	\N	12
335	Optimus	physical	42.6917147	-2.9441209	\N	\N	12
336	Ferretería Peláez	physical	40.4567101	-3.704792	\N	\N	12
337	Asenjo	physical	42.0259884	-3.7611334	\N	\N	12
338	Respuestos Lerma	physical	42.0265688	-3.7613248	\N	\N	12
341	BricHogar	physical	28.6612662	-17.7796197	\N	\N	12
342	Ferretería Tropical	physical	40.2824426	-3.7969501	\N	\N	12
351	Kiñu	physical	43.1861276	-2.4710829	San Juan kalea, 17, 20600, Eibar	\N	12
352	Galeote	physical	40.4582201	-3.4795345	Plaza Mayor, 9	\N	12
353	Comercial Metabos	physical	40.9770018	-5.6544064	Avenida Federico Anaya, 47, Salamanca	http://www.metabos.com/	12
354	Ferretería San José	physical	40.9757785	-5.6554164	\N	\N	12
355	Ferretería Henares	physical	40.4210666	-3.5294173	Plaza de Ondarreta, 28830	\N	12
356	Electrodomésticos Sertec	physical	40.4208566	-3.5309791	Plaza de Ondarreta, 28830	\N	12
357	Reformas Bell	physical	40.4209114	-3.5309999	Plaza de Ondarreta, 28830	\N	12
358	Precoin extintores	physical	40.4210913	-3.5327361	\N	\N	12
359	Maely	physical	40.4282331	-3.5305807	\N	\N	12
360	Administració de loteries	physical	40.5976093	0.4478234	\N	\N	12
361	Cinta's english	physical	40.5969718	0.443305	Plaça catalunya nº 13	\N	12
362	Antoni Rovira serralleria	physical	40.5987862	0.4499053	\N	\N	12
363	Assessoria laboral abic, s.l.	physical	40.5965272	0.4424665	\N	\N	12
364	Cicle-motos Tallada	physical	40.5951818	0.4447444	\N	\N	12
365	Deu telecom	physical	40.5968228	0.4469821	\N	\N	12
366	Sans advocat	physical	40.5974605	0.4434851	\N	\N	12
367	Ferreteria Alfara S. L.	physical	40.5975757	0.4431909	\N	\N	12
368	Bricolatge Tres Cales	physical	40.90803	0.8088389	\N	\N	12
369	AG Grupo Regueira	physical	42.1115296	-8.7646359	Curros Enriquez, 36380	\N	12
370	Assegurances Castell	physical	40.5957642	0.4454687	\N	\N	12
371	Assessoria milian	physical	40.5966335	0.4451671	\N	\N	12
372	Centre Terramar massatges	physical	40.5948928	0.4476469	\N	\N	12
373	Fusteria Enrique Edo Castell	physical	40.6095083	0.3499937	C/ Sant Jeroni, 7, El Castell	\N	12
374	Materials Esteve	physical	40.5987296	0.442173	\N	\N	12
375	Josep martorell rubio	physical	40.5975579	0.4479371	C/ Major, 73	\N	12
376	Armeria Escoto	physical	40.5962649	0.4462539	\N	\N	12
377	Estanc Ollé Labèrnia	physical	40.5962125	0.4463545	\N	\N	12
378	Excavacions Ulldecona	physical	40.5974527	0.4440231	C/Cardenal Gomà, 26 , Ulldecona	\N	12
379	Tecnoprevent	physical	40.5982497	0.4444803	\N	\N	12
380	David Tomàs	physical	40.5956999	0.4446864	Carrer Aragó, 23, 43550, Ulldecona	\N	12
381	Juan Pablo Pascual Villares	physical	40.5987514	0.4439693	\N	\N	12
382	Làpides Riba	physical	40.5986727	0.4498107	C/General Cabrera, 15	\N	12
383	Hobmodel aeromodelismo	physical	40.3226079	-3.8806124	\N	\N	12
384	Ferretería Olivera	physical	39.9837729	-6.5339147	\N	\N	12
385	Valldosera	physical	40.8944959	0.7913977	\N	\N	12
386	Roal	physical	42.3497615	-3.6723104	\N	\N	12
387	Santi 17	physical	43.3241677	-1.9736118	\N	\N	12
388	Setalde	physical	43.324739	-1.9736821	\N	\N	12
389	Ferretería Gros	physical	43.323733	-1.9726768	\N	\N	12
390	Agencia Ferré	physical	40.5967313	0.4480425	\N	\N	12
391	Assessoria Moreno-Roca	physical	40.598421	0.4452629	\N	\N	12
392	Mor & Mor. Design works	physical	40.5938816	0.4451456	\N	\N	12
393	Brau Adell, Lourdes	physical	40.5985958	0.4438119	\N	\N	12
394	Carlos Castell Esteller	physical	40.5977499	0.4424075	\N	\N	12
395	Alfonso Millan Fuentes	physical	40.6004359	0.4471063	c/ Barcelona, S/N	\N	12
396	Consultoria Eugeni, S.L.	physical	40.5984079	0.4432189	\N	\N	12
397	Josep López i Ferré	physical	40.5986123	0.4429254	\N	\N	12
398	Álvaro J. Barrera Favaró	physical	40.5983694	0.4463475	\N	\N	12
399	MCM Assegurances	physical	40.5981109	0.4462017	\N	\N	12
400	Benjamin Sans Biosca	physical	40.6271565	0.3658313	\N	\N	12
401	Mútua General de Seguros	physical	40.5964971	0.4466483	\N	\N	12
402	Sauch-Viladot, S.L.	physical	40.5964253	0.4446676	\N	\N	12
403	Construccions Joan Morcillo S. L.	physical	40.594949	0.4437023	\N	\N	12
404	Solisan, S.L.	physical	40.5961143	0.448441	\N	\N	12
405	Doménech-Subirats, S.C.P.	physical	40.5952699	0.4436151	\N	\N	12
406	Molí Jordi Castell Pla	physical	40.62643	0.3667748	C/ Major, 8	\N	12
407	Obres i contractes Montsià, S.L	physical	40.5971687	0.448412	\N	\N	12
408	Royalsol	physical	40.5967847	0.4500077	\N	\N	12
409	Talleres Elfo	physical	40.5985165	0.4426889	\N	\N	12
410	V.M. Instalec, S.L.	physical	40.5992716	0.4482606	\N	\N	12
411	Taller metàl·lic Manuel Campos	physical	40.5981136	0.4459671	\N	\N	12
412	Sorea	physical	40.5987735	0.4483418	\N	\N	12
413	Talleres Gallardo Moyá	physical	40.5809798	0.4491609	\N	\N	12
414	Moder-Alum	physical	41.4524973	2.2357407	\N	\N	12
415	Kika Bretón. Maderas y decoración	physical	40.4264217	-3.5335735	\N	\N	12
416	Leroy Merlin_5	physical	39.4996685	-0.4086807	Avenida de la Ilustración, 6, 46100, València	\N	12
417	Plastizabal	physical	43.3252076	-1.9714778	\N	\N	12
418	PAC	physical	43.3236686	-1.9712195	\N	\N	12
419	Arjugas	physical	40.4270395	-3.5257788	Calle de Nazario Calonge, 28830	\N	12
420	Ferretería Sandra	physical	39.9194509	-0.5943801	\N	\N	12
421	Ferreteria Alejo	physical	42.688417	-2.9519758	\N	\N	12
422	Adai Carpinteria en Aluminio	physical	41.3946391	2.0101405	\N	\N	12
423	Arevalillo Cristales	physical	40.3891445	-3.7652844	\N	\N	12
424	Ferretería_1	physical	40.3884486	-3.7662737	\N	\N	12
425	Materiales de Construcción Sebastián Álvaro	physical	40.3897867	-3.766043	\N	\N	12
426	Margon	physical	42.8111006	-1.6108246	\N	\N	12
427	Ferretería de San Claudio	physical	43.3600873	-5.9175004	Ponteo - San Claudio, San Claudio	\N	12
429	Boxi	physical	37.7622133	-3.7925508	Calle senda d elos huertos, 9, 23002	http://www.boxijaen.es/	12
430	Linca Ferretería	physical	37.7622391	-3.7923207	Calle Senda de los Huertos, 9, 23002	\N	12
431	Campingmania	physical	37.7655541	-3.7839231	Calle Adarves Bajos, 35, 23001	\N	12
432	Radiluz	physical	37.7669747	-3.7845132	Calle Adarves Bajos, 35, 23001	\N	12
433	Aluminios Martínez	physical	37.7630437	-3.793297	Calle Carrera de Jesús, 39, 23002	\N	12
434	Barchafe	physical	37.7736723	-3.7949502	Calle Millán de Priego, 66, 23007	\N	12
435	Olipublic Tampografía	physical	37.7669175	-3.7844569	Calle Adarves Bajos, 28, 23001	\N	12
436	Aluminios de la Casa	physical	37.7609612	-3.7944753	Calle Juan Montilla, 26, 23002	\N	12
437	Reformas General Juanma	physical	37.7644509	-3.7859275	Fuente de Don Diego, 46, 23002	\N	12
438	oleo-cata xauen	physical	37.7655788	-3.7882554	Calle Muñoz Garnica, 7, 23001	\N	12
439	Puertas Tuñón	physical	37.772026	-3.7920936	Calle Millán de Priego, 22, 23007	\N	12
440	Aluminios y Persianas	physical	37.7594556	-3.7912164	Camino Fuente de la Peña, 61, 23002	\N	12
441	Beltran Montoro	physical	37.7679331	-3.7767348	C/ Carretera de la Guardia, 9, 23003	\N	12
442	Aluminios Hernández Cristalería	physical	37.7600029	-3.7908293	Camino Fuente de la Peña, 41, 23002	\N	12
443	Almacén de barnices y pinturas Julina	physical	37.7602616	-3.7907432	Camino Fuente de la Peña, 37, 23002	\N	12
444	Julio	physical	43.1245143	-8.1420122	\N	\N	12
1284	Hogar	physical	43.25922	-2.9347685	\N	\N	12
445	Ferretería Alonso_1	physical	38.0617578	-0.8673765	Avenida de la Paz, 21, Jacarilla	\N	12
446	Atonio Brito Brito	physical	37.9420328	-5.7607027	\N	\N	12
447	Carpintería Falcón, S.C.	physical	37.9414744	-5.761054	\N	\N	12
448	Ferreteria Los Manantiales	physical	37.9410233	-5.760822	\N	\N	12
449	Barchafe_1	physical	37.7681922	-3.7891673	Calle San Clemente, 9, 23004	https://barchafe.com/	12
450	Gonzalo	physical	42.549143	-3.3240317	\N	\N	12
451	Campomar Suministros	physical	42.5529347	-3.3231902	\N	\N	12
452	Tornillería López Calvo	physical	40.4059173	-3.6977459	Calle de José Antonio Armona, 4, 28012, Madrid	\N	12
480	Juanjo	physical	39.0027963	-1.8653344	\N	\N	12
481	Juanjo_1	physical	38.9958132	-1.8676465	\N	\N	12
482	Juanjo_2	physical	38.9873406	-1.8531783	\N	\N	12
483	Tendero	physical	38.9978897	-1.8606157	\N	\N	12
484	Herlo	physical	38.9956468	-1.8599932	\N	\N	12
485	Jersan	physical	38.9945336	-1.872101	\N	\N	12
486	Rosario	physical	38.9887422	-1.859736	\N	\N	12
487	Agonmar, S.L.	physical	38.987074	-1.8594687	\N	\N	12
488	DM Brico	physical	36.5339334	-4.6329266	\N	\N	12
489	Ferretería tornillería	physical	40.3887205	-3.7318875	\N	\N	12
490	Ferretería Sempere	physical	38.2926424	-0.589081	\N	\N	12
491	Ferretería Mondariz	physical	42.2329905	-8.4559529	\N	\N	12
492	S@t Gescom	physical	42.2639419	-8.78163	\N	\N	12
493	Brico Dépôt_1	physical	43.5049189	-8.2020871	Centro Comercial de O Boial	\N	12
494	Ferretería El Clavo	physical	36.6012896	-4.5324582	Avenida Salvador Vicente, 3, 29631	\N	12
495	Ferreteria Segurvi	physical	41.4202718	2.1493236	Carrer del Santuari, 2, 08023	https://www.segurvi.net/	12
498	Ferreteria Artalejo	physical	42.0517046	3.1927027	\N	\N	12
499	Repuestos Arrebola	physical	37.1970869	-4.0466731	\N	\N	12
500	Morán	physical	43.5356348	-7.0433863	Rúa José Vicente Pérez Martínez, 9, 27700	\N	12
501	Venta de Leña	physical	40.660414	-4.014962	28430, Alpedrete	\N	12
502	Leroy Merlin_6	physical	38.9067564	-6.3510687	\N	\N	12
503	Cal Marimón	physical	41.4509792	1.7029707	\N	\N	12
504	Ferretería Fernández	physical	43.1622871	-5.8295437	\N	\N	12
505	La Bisagra	physical	43.1566715	-5.8282608	\N	\N	12
506	BricoKing	physical	42.5915754	-8.7502632	Vilagarcía de Arosa	\N	12
507	Optimus Ferreteria	physical	41.1979888	1.6249394	\N	https://optimusferreteria.com	12
508	FiR	physical	43.496808	-8.2001724	Rúa Concepción Arenal, 20, Narón	https://www.ferreteriafir.com/	12
509	Fes Mes Bricolatge	physical	41.7257944	1.8457116	\N	\N	12
534	Los Gladiolos	physical	28.4613381	-16.272641	\N	\N	12
535	Veyfra	physical	42.330824	-3.7092107	\N	\N	12
536	Pasayma	physical	40.3451568	-3.7118582	\N	\N	12
537	Aranguren	physical	43.2106373	-3.116168	\N	\N	12
538	Ferretería Pontenova	physical	42.1558904	-8.6194294	\N	\N	12
539	Ferraxaría Patao	physical	42.7806532	-7.8928412	\N	\N	12
540	Bricolaje Rues	physical	43.4609088	-3.8151588	Calle de Fernández de Isla, 25, 39008, Santander	\N	12
541	Centro de Bricolaje y Manualidades	physical	43.4454975	-3.8515196	Avenida de San Martín del Pino, 8, 39011, Santander	http://www.centrodebricolaje.net	12
542	Comercial Quijano	physical	43.4591981	-3.8203287	Calle de Isaac Peral, 34, 39008, Santander	\N	12
543	Electricidad Cosas	physical	43.4630237	-3.7987477	Calle de Hernán Cortés, 30, 39003, Santander	\N	12
544	Electricidad Delgado	physical	43.4640791	-3.8107208	Calle de la Enseñanza, 7, 39001, Santander	\N	12
545	Electricidad Domingo Ruiz	physical	43.4569822	-3.8110403	Calle de Madrid, 16, 39009, Santander	\N	12
546	Electricidad Mayo	physical	43.4631109	-3.8039068	Calle del Medio, 23, 39003, Santander	\N	12
547	Electricidad Plaza	physical	43.458024	-3.8224391	Calle de la Democracia, 1, 39008, Santander	http://www.electricidadplaza.com	12
548	Electricidad Ruiz Abad	physical	43.4653878	-3.7888982	Paseo de Canalejas, 71, 39004, Santander	\N	12
549	Electricidad T.E.E.	physical	43.4604275	-3.8166557	Calle del Tres de Noviembre, 2A, 39010, Santander	http://www.electricidadtee.com	12
550	Elma	physical	43.4632703	-3.8094074	Calle de Luis Hoyos Sainz, 2, 39001, Santander	\N	12
551	Enra Instalaciones Eléctricas	physical	43.4686879	-3.7929458	Paseo de Altamira, 28, 39005, Santander	http://www.instalacionesenra.com	12
552	Ferretería Cubas	physical	43.4640289	-3.8407867	Calle de la Gloria, 56, 39012, Santander	\N	12
553	Ferretería El Herraje	physical	43.4590621	-3.8199735	Calle de Isaac Peral, 23, 39008, Santander	http://www.ferreteriaelherraje.com	12
554	Ferretería Lima	physical	43.4541256	-3.818701	Calle del Marqués de la Hermida, 38, 39009, Santander	\N	12
555	Ferretería Lima_1	physical	43.4586726	-3.8266298	Calle de San Fernando, 88, 39007, Santander	\N	12
556	Ferretería Lima_2	physical	43.4622426	-3.8373834	Calle de la Albericia, 5A, 39012, Santander	\N	12
557	Ferretería Santander	physical	43.4526785	-3.8240108	Calle del Marqués de la Hermida, 72, 39009, Santander	https://www.ferreteriasantander.net/	12
558	Ferretería Seco	physical	43.4622471	-3.8285251	Paseo de Altamira, 306, 39010, Santander	\N	12
559	Ferretería Valdecilla	physical	43.4578907	-3.8283237	Avenida de Valdecilla, 19, 39008, Santander	\N	12
560	Ferretería La Carredana	physical	43.4462513	-3.8325164	Avenida de Parayas, 9, 39011, Santander	http://www.lacarredanasa.es	12
561	Ferretería la Montañesa	physical	43.459087	-3.8281624	Calle de Valentín Lavín Casalís, 22, 39010, Santander	\N	12
562	Ferretería Montañesa	physical	43.4597408	-3.8094104	Calle de Cádiz, 4, 39002, Santander	\N	12
563	Instalaciones Eléctricas Carbe	physical	43.4585746	-3.8212752	Calle Alta, 78B, 39008, Santander	\N	12
564	Luz Cantabria	physical	43.4460978	-3.8558275	Avenida Primero de Mayo, 10-12, 39011, Santander	\N	12
565	Luz Interior	physical	43.4641318	-3.8213481	Paseo de Altamira, 278, 39006, Santander	\N	12
566	Marino de la Fuente	physical	43.4346948	-3.8366661	Calle de las Naos, 1, 39011, Santander	\N	12
567	Seimar Iluminación	physical	43.4544186	-3.817662	Calle del Marqués de la Hermida, 34, 39009, Santander	\N	12
568	Talleres Electro Unión	physical	43.4578532	-3.8187277	Calle del Duque de Ahumada, 6, 39008, Santander	\N	12
569	Talleres Siper	physical	43.4623767	-3.8378178	Calle de la Albericia, 9, 39012, Santander	\N	12
570	Dalia Sistemas S. L.	physical	42.5281217	-7.5083353	Rúa Doutor Casares, 189-191, 27400, Monforte de Lemos	\N	12
571	Ferretería Bricoriol	physical	38.0809261	-0.9444202	\N	\N	12
572	JyJ	physical	28.4662821	-16.2555559	\N	\N	12
573	Repuestos Mineros	physical	28.4673107	-16.2546668	\N	\N	12
456	Ple de Tallers	physical	41.4816266	2.3243834	Passatge Sant Jaume, 2, 08320	http://www.pledetallers.com	12
457	Materiales Renau	physical	39.9490087	-0.0599907	\N	\N	12
458	Eurometal Campet	physical	38.3836133	-0.7614748	Capellà Margall, 5, 03660, Novelda	\N	12
459	Agritec	physical	38.377857	-0.7709343	\N	\N	12
460	Aliban	physical	38.3811953	-0.7733616	\N	\N	12
461	Herrería Martínez	physical	38.3775164	-0.7715328	\N	\N	12
462	Novelforja	physical	38.3811602	-0.7738905	\N	\N	12
463	Segura S.L	physical	38.377206	-0.7710231	\N	\N	12
464	Carpintería metálica	physical	38.3840612	-0.7761456	\N	\N	12
465	Ideatec	physical	38.3842578	-0.7761238	\N	\N	12
466	MBS Carpintería	physical	38.3856627	-0.7772365	\N	\N	12
467	Suministros Industriales	physical	38.384356	-0.7691067	calle San Roque, 10	\N	12
468	Belsan	physical	38.3894729	-0.7675796	\N	\N	12
469	Alunovel	physical	38.381353	-0.7656247	\N	\N	12
470	Kriset	physical	38.3814845	-0.7671061	\N	\N	12
471	A Pedals Novelda	physical	38.3813358	-0.7627988	\N	\N	12
472	Ferretería_2	physical	37.9934776	-1.1267232	\N	\N	12
473	Ferreteria Santa Margarida	physical	42.2657023	3.1511723	\N	\N	12
474	Ferretería Agudo	physical	43.3864577	-3.7288366	Barrio La Rañada, 39716, El Bosque	\N	12
475	Agro - Cobima	physical	40.4272905	-3.5378215	\N	\N	12
476	Plaza Mayor	physical	38.9951504	-1.8587384	\N	\N	12
477	Ferretería Juanjo	physical	38.9888339	-1.8484328	\N	\N	12
478	Ferretería_3	physical	38.9180982	-1.9183101	\N	\N	12
479	Ferretería La Moneda	physical	37.2903108	-5.9259336	\N	\N	12
496	Ferreteria Bofí	physical	39.0351824	-0.2173792	\N	\N	12
497	Ferreteria Mañá	physical	39.0347757	-0.218609	\N	\N	12
510	Ferretería Hervás	physical	40.2726546	-5.8615332	\N	\N	12
511	Ramón Portus	physical	38.1935722	-0.5611691	\N	\N	12
512	Pintures Illa	physical	41.9801006	2.8133213	\N	\N	12
513	Cadena Els Tigres	physical	41.4106854	2.1381335	\N	\N	12
514	Motos Romero	physical	43.4898966	-8.1964921	\N	\N	12
515	Almacenes El Pilar	physical	40.3221657	-3.8691279	\N	\N	12
516	Ferretería El Ortigal	physical	28.4718033	-16.3711356	\N	\N	12
517	Ferretería La Salle	physical	28.4617648	-16.2571034	\N	\N	12
518	Ferretería Sanmartín	physical	39.4824975	-0.4432436	\N	\N	12
519	Ferretería San Bartolomé	physical	28.4588371	-16.3080638	\N	\N	12
520	Garrido Fuentes	physical	40.0860401	-6.3518426	\N	\N	12
521	Ferretería_4	physical	38.1285259	-0.8771775	\N	\N	12
522	Piscinas Costa Cálida	physical	37.6282494	-1.038098	\N	\N	12
523	Telleri	physical	43.3807255	-2.9834682	\N	\N	12
524	La Pinta	physical	39.3830996	-6.2488928	\N	\N	12
525	Bricoplant	physical	37.1986584	-4.0464968	Calle San Juan, 18360, Huétor Tájar	http://www.jardineriavalenzuela.com/	12
526	Ferretería El Carmen	physical	37.1972456	-4.0475092	Calle Ancha, 55, 18360, Huétor Tájar	\N	12
527	Ferretería Meda	physical	42.6744669	-8.8255136	Campos de Pazos, Rianxo	\N	12
528	El Hórreo	physical	42.910867	-8.7368188	Rúa da Cachurra, 15830, Negreira	\N	12
529	Tucho	physical	42.6477008	-8.8792644	\N	\N	12
530	Jeloal	physical	42.6483235	-8.8852653	\N	\N	12
531	Ferretería Bosch	physical	38.843249	0.0097081	Carrer Calvari, 3, 03770, el Verger	\N	12
532	Ferretería Ed	physical	40.4110567	-3.6986309	\N	\N	12
533	Ferreiro	physical	42.9093979	-8.7349065	\N	\N	12
577	Larrieta	physical	43.3023854	-3.0345617	\N	\N	12
578	Case Maquinaria de ocasión	physical	40.2374732	-3.6890519	\N	\N	12
579	Hogar & Hobby	physical	40.407053	-3.6481835	Avenida de Moratalaz, 141, 28030, Madrid	\N	12
580	Findetosa Ferretería	physical	39.868752	-4.0216674	Calle Marqués de Mendigorría, 17, 45003, Toledo	\N	12
581	Cafosa Fontanería	physical	39.8686928	-4.0216879	Calle Marqués de Mendigorría, 17, 45003, Toledo	\N	12
582	Bricomat	physical	41.8546145	-1.9209185	\N	\N	12
583	Omeñaca	physical	41.8547331	-1.9207017	\N	\N	12
584	Xerox	physical	40.4556942	-3.6925434	\N	\N	12
585	Milera	physical	43.3079373	-4.2371441	\N	\N	12
586	Decoración Ancor	physical	40.4265946	-3.5319917	\N	\N	12
587	Leroy Merlin_7	physical	40.5304099	-3.6464256	\N	\N	12
588	Azulejos y Baños Mart-Home	physical	39.8687301	-4.0233735	Avenida del General Villalba, 14, 45003, Toledo	http://www.azulejosybanosmarthome.es	12
589	Sumferrsán	physical	40.3829895	-3.7641857	Calle del Damasquillo, 1, 28044, Madrid	\N	12
590	Ferreteria Mena	physical	39.4571167	-5.8810734	\N	\N	12
591	Ikatz	physical	43.3039488	-3.0356093	\N	\N	12
592	Ferretería Llaves	physical	39.8591986	-4.0231393	Calle de la Plata, 24, 45001, Toledo	\N	12
593	Venecia	physical	40.4263088	-3.706803	Calle de San Bernardo, 64, 28015, Madrid	http://www.veneciaferreterias.es	12
600	Ferreteria Luma	physical	41.4165017	2.1952104	Carrer de Huelva, 54, 08020, Barcelona	\N	12
601	Gama Radio	physical	40.4242393	-3.7061681	Calle de Minas, 4, 28004, Madrid	\N	12
602	Javier	physical	40.4641192	-3.4628086	\N	\N	12
603	Ferretería Delgado	physical	38.2392812	-6.0128724	Avenida Jesús de Nazaret, 16	\N	12
604	Cuchillería Garrido	physical	39.8581554	-4.0214639	Calle Horno de los Bizcochos, 13, 45001, Toledo	\N	12
605	Juan del Rosario	physical	28.3134831	-16.4116631	\N	\N	12
606	Ferreteria Abando	physical	43.2651279	-2.9309539	\N	\N	12
607	Maquinària Pau	physical	42.2491074	2.9607718	\N	\N	12
608	Rucho	physical	43.0172168	-7.5604366	Avenida da Coruña, 80, 27003, Lugo	\N	12
609	la ferretería	physical	42.1603525	-8.6203711	\N	\N	12
610	Cadena 88	physical	41.4125105	2.1396329	\N	\N	12
611	Ferreteria Nova	physical	39.705156	2.7957318	\N	\N	12
612	Muneratibi	physical	42.9674724	-8.443761	Rúa Camiño Real, 20, Sigüeiro	https://www.muneratibi.com/	12
613	Ferretería Moncarbal	physical	43.394351	-5.7037247	\N	\N	12
614	Eco-Pintura	physical	36.1293393	-5.4461269	\N	\N	12
615	Ferretería Sánchez	physical	43.1508188	-8.3863184	\N	\N	12
616	Avenida	physical	37.9133451	-3.124214	\N	\N	12
617	Francisco Gomez	physical	37.9113182	-3.1290577	\N	\N	12
618	Martínez Trillo	physical	37.9132154	-3.1321595	\N	\N	12
619	Suministros agrícolas	physical	37.9455741	-2.9547024	\N	\N	12
620	Bello	physical	37.9141985	-3.1282053	\N	\N	12
621	Carpintería Ortuño	physical	37.9137796	-3.1285636	\N	\N	12
622	Materiales de Construcción	physical	37.9465473	-2.9549423	\N	\N	12
623	Materiales y ferretería Castillo	physical	37.9188607	-3.0061589	\N	\N	12
575	Repuestos de electrodomésticos Radel	physical	40.3351139	-3.767906	\N	\N	12
576	Procalor	physical	28.4515079	-16.2955592	\N	https://www.procalor.es/	12
594	Mariano	physical	40.4201534	-3.6146972	\N	\N	12
595	Leroy Merlin_8	physical	36.7754227	-2.6131897	Carretera de Alicún, 04740, Roquetas de Mar	\N	12
596	Loymar	physical	41.9021641	-8.8694857	\N	\N	12
597	Cristosa	physical	40.5775654	-3.9299949	\N	\N	12
598	Suministros La Guía	physical	42.1461859	-8.6225376	\N	\N	12
599	FontaGuía	physical	42.1499621	-8.6222127	\N	\N	12
624	Carpinteria Metalica Barriche	physical	37.9202423	-3.0235703	\N	\N	12
625	Carpinteria Muñoz y Escribano	physical	37.9181779	-3.0224544	\N	\N	12
626	Preyser	physical	38.4864174	-0.7889087	\N	\N	12
627	Ferretería Agroquímicos Lava	physical	37.8464938	-3.0684936	\N	\N	12
628	Ferreteria_2	physical	37.8457854	-3.0679795	\N	\N	12
629	Repuestos Aranda	physical	37.8464691	-3.0697627	\N	\N	12
630	Taller de Cerámica "J.M. Morata"	physical	37.8464596	-3.0693957	\N	\N	12
631	ferreteria yanes	physical	43.6845832	-7.8513482	\N	\N	12
632	Ferretria Farrenou	physical	42.4077291	0.7405044	\N	\N	12
633	La Nueva	physical	36.1290945	-5.4460542	\N	\N	12
634	Ferretería Gil Cánovas	physical	38.3476832	-0.7670774	\N	\N	12
635	La Palmera	physical	37.9138273	-3.118092	Avenida de Andalucía, 41, 23460, Peal de Becerro	\N	12
636	Tall Fi	physical	41.9792375	2.811713	\N	\N	12
637	Torno y Fresa Modroño	physical	40.024725	-3.8541216	\N	\N	12
638	Ferretería Chávez	physical	28.4962888	-16.3779517	Carretera de El Boquerón, 44, 38330, Guamasa	http://ferreteriachavez.es	12
639	Almacenes Mori	physical	43.4848644	-5.270625	\N	\N	12
640	Torno y Fresadora Lozano	physical	40.025354	-3.8569023	\N	\N	12
641	Gogar	physical	40.3991392	-3.6196152	Calle del Cordel de Pavones, 34, 28032, Madrid	\N	12
642	Ferreteria Mariñel	physical	43.3615334	-1.7971228	\N	\N	12
643	Cazorla	physical	37.9127151	-3.0037419	Avenida Cronista Lorenzo Polaino, 23470, Cazorla	\N	12
644	Ferretería Rojas	physical	37.911811	-3.0028461	Calle Doctor Muñoz, 9, 23470, Cazorla	\N	12
645	Ferreteria Consell	physical	39.6693659	2.814676	\N	\N	12
646	Ganivets Joan Campins	physical	39.6704353	2.8167467	\N	\N	12
653	Hnos. García Moyano	physical	40.9686855	-5.648239	\N	\N	12
654	Ferretería Madrid	physical	40.968371	-5.6478757	\N	\N	12
655	Ferretería Pascual_1	physical	38.9942955	-1.8630733	\N	\N	12
656	Suministros Viangea	physical	38.0882876	-0.9754052	\N	\N	12
657	Ferrocano	physical	38.1202291	-1.3031353	\N	\N	12
661	Leroy Merlin_9	physical	40.4467338	-3.6976548	\N	\N	12
662	La Clau	physical	41.4039925	2.2035749	Carrer de Pujades, 233, 08005	\N	12
663	Ferretería Fuenlabrada	physical	40.2830586	-3.7889247	\N	\N	12
664	Cosas para hacer Casas	physical	40.4602836	-3.7006868	Calle de los Algodonales, 13, 28039, Madrid	\N	12
665	Ferretería Diego	physical	40.4025927	-3.6434679	\N	\N	12
666	Gogar_1	physical	40.4074313	-3.6497939	Calle de la Marroquina, 15, 28030, Madrid	\N	12
667	Diego	physical	40.410352	-3.6516492	Calle del Camino de los Vinateros, 65, 28030, Madrid	\N	12
668	Jin perlas	physical	36.5518229	-4.6154625	\N	\N	12
669	Puertas Valero	physical	38.9977593	-1.8558495	\N	\N	12
670	Fernando	physical	38.9963668	-1.8545003	\N	\N	12
671	Ferretería Avenida	physical	40.5395724	-4.1608335	\N	\N	12
672	Las Ciencias	physical	37.4023602	-5.925886	\N	\N	12
673	Brico Marc	physical	37.1370612	-3.6605641	\N	\N	12
680	Chamaco	physical	42.0518679	-6.6337035	\N	\N	12
683	Ferretería Olid	physical	38.5355541	-0.1066658	\N	\N	12
684	Brihuega azulejos y pavimentos	physical	40.2719288	-3.7526107	\N	\N	12
685	Hernán García Electricidad	physical	40.251603	-3.8297168	\N	\N	12
686	Molina	physical	37.980191	-0.6698873	\N	\N	12
687	Ferreteria Electro Europa - Optimus	physical	41.4075397	2.1608766	Carrer de l'Escorial, 35, 08024, Barcelona	https://www.electroeuropa.com	12
688	Benidorm	physical	40.4259742	-3.6787934	Calle de Hermosilla, 70, 28001, Madrid	\N	12
689	Printhatshit	physical	41.378011	2.1331685	Carrer de Papin, 26, 08028, Barcelona	http://www.printhatshit.com/	12
690	Ferreteria i Parament Ca La Maria	physical	41.4895426	2.3573712	\N	\N	12
691	La Pixuela	physical	43.5590991	-6.1501282	\N	\N	12
692	Sergio	physical	43.5592179	-6.149226	\N	\N	12
696	Electro-Manga	physical	37.6485572	-0.7158938	\N	\N	12
697	Espinosa	physical	40.4737986	-3.7184016	\N	\N	12
698	Venecia_1	physical	40.4270456	-3.7014727	\N	\N	12
699	Ferretería Moreno	physical	37.690778	-1.0711882	Plaza de la Iglesia, 30390, La Aljorra	\N	12
700	Pinmat S.A.	physical	41.5370997	2.4387865	Carrer del General Torrijos, 5 - 33, 08302, Mataró	\N	12
701	Bestard	physical	39.7143846	3.4599126	\N	\N	12
702	Ferretería Segura García	physical	36.9404167	-2.1377214	\N	\N	12
703	Ferreteria Torres	physical	41.4403225	2.2259247	Carrer de Nàpols, 20, Badalona	https://ferreteriatorres.es/	12
704	Casa	physical	36.5913258	-6.2224063	\N	\N	12
705	EM Home Market	physical	36.5910946	-6.2223684	\N	\N	12
706	Ferretería Reina Mercedes	physical	37.356577	-5.9859867	Calle Levante, 1, 41012, Sevilla	\N	12
707	Ibai Ondo	physical	43.1689951	-2.5735116	Iturritza	\N	12
708	Ferretería Titanio	physical	42.7376092	-8.6606346	Rúa Longa, 32	\N	12
709	Ferro Gomera	physical	28.0880402	-17.3351308	\N	\N	12
710	Leroy Merlin_10	physical	38.7320025	-0.4429448	\N	\N	12
722	Revestimientos Jaén	physical	40.2220484	-3.8469343	\N	\N	12
723	Hilti	physical	40.275454	-3.8068457	\N	https://www.hilti.es/	12
724	Ferretería Ruilopez	physical	40.2854218	-3.8077383	\N	\N	12
725	Brico Aitana	physical	38.6452173	0.0519023	\N	\N	12
726	Ferretería d'Alaró	physical	39.7070709	2.7889838	\N	\N	12
727	Cofac-Ferbikes Prats S.L.	physical	42.0054114	2.0337406	\N	\N	12
728	Comercial Lluçanès	physical	42.0082431	2.0307255	\N	\N	12
729	Leroy Merlin_11	physical	41.4412809	2.1989235	Paseo Portesí, 2	https://www.leroymerlin.es	12
730	Ferreteria Carreras	physical	39.9320718	4.1374529	Carrer Miguel de Cervantes, 21B, 07730, Alaior	\N	12
731	Palliser	physical	39.9310591	4.1369635	Carretera Nova, 22, 07730, Alaior	\N	12
750	La Ferretería_1	physical	37.3436014	-5.9802242	Avenida de Finlandia	\N	12
751	Ferretería Tropical_1	physical	40.281497	-3.8087044	\N	\N	12
752	Materiales de Construcción Aranguren	physical	43.2114712	-3.1136424	\N	\N	12
647	Comercial Borrell	physical	42.2566801	2.9685338	\N	\N	12
648	IMA	physical	42.2617507	2.9670872	\N	\N	12
649	Ferreteria Ferrohogar	physical	38.7300461	0.1446229	Carrer de les Capelletes, 03720, Benitachell/el Poble Nou de Benitatxell	\N	12
650	La Herradura	physical	43.3000577	-7.6775417	\N	\N	12
651	BricoKing_1	physical	43.2999956	-7.6777002	\N	\N	12
652	Puentes	physical	43.2985746	-7.6806358	\N	\N	12
658	Bricolage Madrid	physical	40.4574605	-3.7064049	\N	\N	12
659	Garosa	physical	42.6858866	-2.9427918	\N	\N	12
660	Family beer	physical	41.4061051	2.1594802	Carrer de Joan Blanques, 53, 08024	https://family-beer.com/	12
674	El Tanque	physical	28.3553221	-16.7830189	\N	\N	12
675	Ferreteria Ferrokey	physical	38.4135518	-0.442933	\N	\N	12
676	Ferretería Alonso_2	physical	40.4880357	-3.6626975	\N	\N	12
677	Ferretería El Parque	physical	40.4765138	-3.7061183	\N	\N	12
678	Cepisa	physical	40.4442691	-3.7038278	\N	\N	12
679	J.A. Bilbao	physical	43.3804345	-2.981082	\N	\N	12
681	Ferretería La Campiña	physical	40.700732	-3.4334432	\N	\N	12
682	Ferretería Brycomil	physical	40.700989	-3.4332336	\N	\N	12
693	Luis	physical	42.9703274	-3.7870478	\N	\N	12
694	ferretería Comercial Candelas	physical	41.6449835	-0.8642914	\N	\N	12
695	Ferreteria Gutierrez	physical	43.2515859	-5.7731246	\N	\N	12
711	Fransalma Ferretería	physical	37.6887024	-1.0680416	\N	\N	12
712	Bricoestació	physical	41.6763699	2.7745134	Avinguda d'Europa, 2, 17310, Blanes	https://www.bricoestacio.com/	12
713	Can Xic	physical	39.6490879	2.772613	avinguda Jaume III, 19, 07320, Santa Maria del Camí	\N	12
714	Magatzem Can Gamundí	physical	39.6510732	2.7714748	carrer Tomàs Forteza, 10, 07320, Santa Maria del Camí	\N	12
715	BdB Esteso	physical	39.6484395	2.7795925	carrer Nadal Batle, 07320, Santa Maria del Camí	\N	12
716	Tavema	physical	39.932529	4.1348334	Carretera Nova, 07730	http://www.tavema.com/	12
717	Rigasa	physical	42.2647407	2.973777	\N	http://www.rigasa.com/	12
718	Ymbert Electrodomèstics	physical	42.264365	2.9839979	\N	http://www.ymbert.es/	12
719	Ferreteria Torres_1	physical	41.7431636	1.8041627	\N	\N	12
720	Comercial Alor	physical	38.2379875	-6.0155372	Calle Bodegones, 2, 06900, Llerena	\N	12
721	Fontanería OIC	physical	40.2206639	-3.847106	\N	\N	12
732	BricoKit A Xesta	physical	43.0029453	-7.5474527	Rúa Rei Don García, 27002, Lugo	\N	12
733	Ferretería-Bazar Pablo	physical	43.002873	-7.5476394	\N	\N	12
734	Ferretería_5	physical	39.3373499	-5.4899236	\N	\N	12
735	Ferretería Industrial Bricolaje	physical	40.2422287	-3.8357256	\N	\N	12
736	Ferretería Esin, SA	physical	40.2745389	-3.7599906	\N	\N	12
737	Cuchilleria Regina	physical	37.3940899	-5.9915445	\N	\N	12
738	Leroy Merlin Compact Oleiros	physical	43.3211571	-8.3168887	\N	\N	12
739	+led	physical	42.216248	-8.7392323	Avenida da Florida	\N	12
740	Ferretón	physical	42.2153551	-8.7405374	Avenida da Florida, 105, 36210, Vigo	\N	12
741	Puerta Carmona	physical	37.3894101	-5.9848771	Puerta de Carmona, 1, 41003, Sevilla / Casco Antiguo / San Bartolomé	\N	12
742	Bricolage Easo	physical	43.339031	-1.7854367	\N	\N	12
743	Saneamientos Pereda	physical	40.3853506	-3.7203538	\N	\N	12
744	Ferretería Irisarri	physical	40.3893411	-3.7295734	\N	\N	12
745	Ferretería Margallo	physical	40.4606341	-3.696151	Calle del General Margallo, 18, 28020	\N	12
746	Ferretería Gabilondo	physical	43.3401872	-1.7908405	\N	\N	12
747	Ferreteria Font Freda	physical	38.8384847	-0.5188392	\N	\N	12
748	Ferretaría Almonte	physical	28.5135126	-16.3050748	Carretera del Monte de las Mercedes, 10, 38293, San Cristóbal de La Laguna	\N	12
749	Maderas Ramos	physical	40.3568395	-4.3426285	Calle del Hilero, 33, 28696, Pelayos de la Presa	http://maderasramos.com/	12
798	Ferretería Viana	physical	37.1606189	-3.5945579	\N	\N	12
799	Hierros Delta	physical	40.7675651	0.6472566	N-340, 43894	https://hierrosdelta.com/	12
800	Ferreteria y Construcción Jurado	physical	36.2108184	-5.4299059	\N	\N	12
801	Ferretería José Santamaría	physical	42.9367433	-3.5750963	Calle Laín Calvo, 24	https://cadena88.com/es/store/santamaria	12
802	Ferro Naval	physical	37.6146887	-0.9889656	\N	\N	12
803	Ferretería Deva	physical	43.3633441	-5.8617886	\N	\N	12
804	Ferretería El Barco	physical	43.3635703	-5.8614886	\N	\N	12
805	Rigau_1	physical	41.9820005	2.8179819	\N	\N	12
806	Encofrados J. Alsina, S.A	physical	41.494414	2.1891798	\N	\N	12
807	La Plataforma de la Construcción	physical	39.4729202	-0.4321467	\N	\N	12
808	Camvaz	physical	43.3748008	-4.4981156	Barrio Lansar, Pesués	\N	12
809	Hiper Euro (Chinese general store)	physical	28.4657839	-16.2702107	Avenida de Venezuela, 13, 38007, Santa Cruz de Tenerife	\N	12
810	Servei Estació_1	physical	41.9831182	2.8192567	Carrer de la Sèquia, 20, 17001, Girona	\N	12
811	Agromaquinaria Moruno	physical	38.2633984	-5.6792683	\N	\N	12
812	T. Martín	physical	41.6983189	-3.9298496	\N	\N	12
813	Marchirant	physical	38.2653654	-5.6820209	\N	\N	12
814	Agrícola Cipriano	physical	38.2617777	-5.6916564	\N	\N	12
815	Ramon Soler	physical	41.664217	0.5546221	\N	\N	12
816	Ferrehogar	physical	42.1308857	-0.4058946	\N	\N	12
817	Ferretería Olazabal	physical	43.3383646	-1.7960204	Serapio Múgica, 15, 20302, Irun	\N	12
818	Ferreteria La Playa	physical	28.1830173	-16.8175812	\N	\N	12
819	Suministros Trápaga	physical	43.3053464	-3.0374102	\N	\N	12
820	Bazarot e Hijos | Materiales de Construcción, Cubas y Ferretería en Sevilla	physical	37.3805392	-5.9368184	Calle San José de Palmete, 11, 41006, Sevilla	https://bazarotehijos.com/	12
821	Ferretería Ventura	physical	41.4935735	2.1349933	\N	\N	12
822	Ferreteria Sartaguda	physical	42.3821054	-2.0573433	\N	\N	12
823	CECOSHOP	physical	37.1334568	-5.4529839	\N	\N	12
824	Ferretería Martín	physical	36.5985399	-4.5347978	\N	\N	12
825	Ferretería Bricolaje Dols	physical	39.4756962	-0.3848293	Carrer de Quart, 64, 46008, València	https://www.ferreteriadols.com/	12
826	Ferretería Els Cunyats	physical	39.476757	-0.3809826	Plaça de Vicent Iborra, 2, 46003, València	\N	12
827	Espronceda	physical	40.4396586	-3.6985767	\N	\N	12
828	Romeu	physical	43.346974	-8.2057769	\N	\N	12
829	Ferretería Delicias	physical	40.4013578	-3.6940987	Paseo de las Delicias, 46, 28045, Madrid	http://www.ferreteriadelicias.es	12
830	Lanas Katia	physical	36.5980312	-4.5351648	\N	\N	12
831	Euskal Ferr	physical	43.3413835	-1.799307	Javier Esteban Indart, 1, 20301, Irun	\N	12
753	Yañez Ferretería e Materiais de Construcción SL.	physical	43.1906617	-8.0251691	\N	\N	12
754	Cuchillería Yáñez	physical	40.9653476	-5.6619724	Calle Correhuela, 10, Salamanca	\N	12
755	Roma	physical	37.3883231	-6.0007938	Calle Reyes Católicos, 12, Sevilla	\N	12
756	Ferretería Marqués de Paradas	physical	37.3887826	-6.0008945	Calle Marqués de Paradas, Sevilla	\N	12
757	Lloan	physical	42.2481149	0.9680512	Avinguda de Verdaguer, 14, 25500, la Pobla de Segur	\N	12
758	Cadena 88_1	physical	40.4733555	-3.6367587	\N	\N	12
759	Saneamientos La Económica	physical	40.4743211	-3.6410575	\N	\N	12
760	Comercial Itolegui	physical	42.9780964	-1.366767	Barrio Santiago, 12, 31694, Aurizberri/Espinal	\N	12
761	Ferreteria Battle	physical	42.0552791	3.1994419	plaça de l'Esglesia, 17258, L'Estartit	\N	12
762	Ferretería Rosin	physical	40.9770269	-5.6759833	\N	\N	12
763	Francisco Aspa	physical	41.796623	2.2189913	\N	\N	12
764	Galerías de Hogar ADLI	physical	39.724729	-4.6410697	\N	\N	12
765	Mundo Detector	physical	40.5043422	-3.8899116	\N	https://www.mundodetector.com/	12
766	Cefera	physical	40.3143919	-3.8564471	\N	\N	12
767	Hiper China	physical	36.879128	-5.406293	\N	\N	12
768	Brico Acoil	physical	37.1754565	-3.6017554	Calle Alhóndiga, 37, 18002, Granada	https://shop.bricoacoil.com/	12
769	Roycha	physical	42.3508297	-3.6698353	\N	\N	12
770	Ferretería La Llave	physical	28.4632775	-16.2624434	Calle de Bernardino Semán, 16, 38005, santa Cruz de Tenerife	http://www.ferreterialallavetenerife.es/	12
771	Droguería Arantza	physical	43.334494	-1.7891171	\N	\N	12
772	Ferretería Felaez	physical	40.4318437	-3.6564107	\N	\N	12
773	Bazar Nuevo	physical	38.259485	-5.6781112	\N	\N	12
774	Ferretería_6	physical	38.2606717	-5.6787525	\N	\N	12
775	Bazar Gómez	physical	38.2595317	-5.6782152	\N	\N	12
776	Talleres Martín	physical	38.2611748	-5.6900265	\N	\N	12
777	Agroazuaga	physical	38.2611609	-5.6883914	\N	\N	12
778	Arance	physical	40.3353284	-3.5319133	\N	\N	12
779	Leroy Merlin_12	physical	42.0125357	-4.5184731	Avenida de Brasilia, 5, 34004, Palencia	\N	12
780	Suministros Ebro-Miranda	physical	42.6917729	-2.9438409	\N	\N	12
781	Fesmés	physical	41.6777255	2.7782226	\N	\N	12
782	ferrCASH	physical	40.4571423	-3.6924076	\N	\N	12
783	Almacenes Jerocer	physical	38.2555048	-5.6803284	\N	\N	12
784	Arrones	physical	37.1302468	-5.4539691	\N	\N	12
785	Magatzems del Centre	physical	42.1807424	2.4890397	\N	\N	12
786	Cuchilleria Ibáñez	physical	42.3410906	-3.7005977	Calle Carnicerías, 16, 09003	\N	12
787	Almacenes Monterrubio	physical	38.2587285	-5.6800198	\N	\N	12
788	Casa Coll	physical	41.9789778	2.8223996	\N	\N	12
789	Rigau	physical	41.9795398	2.8221623	\N	\N	12
790	La Ferretería Extremeña	physical	40.0281748	-6.0898339	\N	\N	12
791	Ferreteria Rocori	physical	42.093558	1.8238794	\N	\N	12
792	Ferretería Fuentes	physical	38.236009	-6.0148304	\N	\N	12
793	A. Muriel	physical	43.3392532	-1.7978752	\N	\N	12
794	Informatica DJ - Programadores	physical	37.3400636	-5.8317286	Murillo, 41550, Alcalá de Guadaíra	http://informaticadj.com	12
795	Nueva Ferretería	physical	38.2657392	-0.6977265	carrer de la Victòria, 3, Elche/Elx	\N	12
796	Ferretería La Fuente	physical	40.4882311	-6.1119524	\N	\N	12
797	Ferretería Sánchez_1	physical	40.9696312	-5.6654535	Paseo de Carmelitas, 20,22, Salamanca	\N	12
852	Ferretería_7	physical	40.4182756	-3.5724758	\N	\N	12
853	Ferretería J-DIN	physical	40.500682	-4.421639	Calle de Cervantes, 1	\N	12
854	Ferretería Álvaro	physical	40.4728833	-3.7117745	\N	\N	12
855	Comercial Anaya	physical	40.8262501	-5.5122979	Calle Álamo Salazar, 15	\N	12
856	Ferretería Carral	physical	43.2267549	-8.3559475	\N	\N	12
857	Sumiagro SL.	physical	43.2271091	-8.3549564	\N	\N	12
858	Provesa	physical	43.2270357	-8.3547448	\N	\N	12
859	Materiales de Construcción Hermanos Gómez	physical	40.8226861	-5.5142868	\N	\N	12
886	Deluxe	physical	42.8161173	-1.6591677	\N	\N	12
887	Ferreteria Correoso	physical	41.4498545	2.2193318	Plaça del Rellotge, 9, 08923, Santa Coloma de Gramenet	\N	12
888	Garrido	physical	42.3909304	-8.7021505	Avenida Jaime Janer, 20	\N	12
894	Ferreteria Sans	physical	41.6119459	0.6299672	Carrer del Bruc, 19, 25001, Lleida	\N	12
895	Bricohogar	physical	38.2473325	-2.7262297	\N	\N	12
896	Ferretería Vieites	physical	43.1516091	-8.3834453	\N	\N	12
897	Ferretería Membrives	physical	40.3962215	-3.7166344	Calle de Lola Membrives, 8, 28019, Madrid	https://ferreteriamembrives.es/	12
898	Ferretería Bricohogar	physical	38.3173909	-2.6617045	\N	\N	12
899	Electrofassar	physical	39.5573812	-0.3284604	\N	\N	12
900	Ferretería Vidal	physical	42.7855503	-1.6894267	\N	\N	12
901	Ferretería Luna	physical	38.3541383	-2.8031274	\N	\N	12
902	Resopal	physical	40.4384375	-3.6193552	Calle de Cronos, 14	\N	12
903	Bricolage PapelHogar	physical	40.4100298	-3.7096412	\N	\N	12
904	Ferretería Zamora	physical	37.764687	-3.0774523	\N	\N	12
905	Ferretería Linares	physical	38.1799398	-3.6901583	\N	\N	12
906	Azulejos Peña	physical	40.4384462	-3.7029662	\N	\N	12
907	Ferretería Embajadores	physical	40.4033823	-3.7015255	Calle de Embajadores, 86, 28012, Madrid	\N	12
908	Ferretería_8	physical	39.8018876	-5.1735408	\N	\N	12
909	Ferretería Puente	physical	39.8022503	-5.1728219	\N	\N	12
910	Ferretería FERGUMAR	physical	39.8060026	-5.1756141	\N	\N	12
911	Ferre-Electro	physical	39.8044319	-5.1718046	\N	\N	12
912	Carlos	physical	41.9154723	3.1680458	\N	\N	12
913	Arias	physical	40.4849504	-3.6995112	\N	\N	12
914	Comercial Pazos	physical	40.3977957	-3.6969722	Calle de Jaime I El Conquistador, 129, 28045, Madrid	\N	12
915	Magago	physical	37.9877307	-3.5237564	\N	\N	12
916	FerrCash	physical	40.4295369	-3.5293787	\N	\N	12
917	Los Abuelos	physical	41.6098746	-4.7071493	Calle del Plomo, 8, 47012, Valladolid	\N	12
918	Ferretería Ruiz	physical	37.6471166	-3.9063793	\N	\N	12
919	Maquinaría Agrícola Liste Galicia	physical	43.0202347	-8.4299816	\N	https://www.liste.es/	12
920	Ferroisora	physical	28.2081991	-16.7765366	\N	\N	12
921	Ferroisora_1	physical	28.2086392	-16.7777515	\N	\N	12
922	Higinio Tabares e Hijos	physical	28.2106893	-16.7814416	\N	\N	12
938	New Planet Home	physical	41.3773215	2.1213673	\N	\N	12
939	Ferreteria Rodríguez	physical	41.3721322	2.1267479	Carrer de la Riera Blanca, 105-107	https://www.cadena88.com/es	12
940	Jardinería Santa Comba	physical	42.1587753	-8.6218147	\N	\N	12
832	Ferretería Guma	physical	40.268954	-3.9190722	\N	\N	12
833	Febrisur	physical	36.6000163	-4.5436416	\N	\N	12
834	Ferretería Minerva	physical	36.5962444	-4.5267111	\N	\N	12
835	Blink	physical	41.98222	2.8223786	\N	\N	12
836	Casa Boué	physical	41.9826291	2.8229449	\N	\N	12
837	Burgalesa	physical	42.3526142	-3.6592885	\N	\N	12
838	Instalaciones eléctricas	physical	40.1898815	-3.8396256	\N	\N	12
839	Azulejos	physical	39.9402018	-4.43806	\N	\N	12
840	Ferriluz	physical	39.9404012	-4.4383127	\N	\N	12
841	Ferretería Castañal	physical	43.4276905	-7.3629959	\N	\N	12
842	Salvador	physical	38.0572862	-1.2071128	\N	\N	12
843	Ferretería Fersán	physical	42.4048407	-8.7492539	\N	\N	12
844	Ferretería Villar	physical	42.4039058	-8.7510929	\N	\N	12
845	Mantenimiento de piscinas	physical	40.3309282	-3.8630413	\N	\N	12
846	Ferretería Brico Bay	physical	40.3325971	-3.8625972	\N	\N	12
847	Instalaciones Dávila	physical	40.3325313	-3.8610984	\N	\N	12
848	Moral manualidades	physical	40.3329914	-3.8616821	\N	\N	12
849	Ferretería electrodomésticos Crespo	physical	40.1081357	-3.3886576	\N	\N	12
850	Ferretería y electrodomésticos Crespo	physical	40.1081239	-3.3887565	\N	\N	12
851	Ferretería Sevillano	physical	37.3821403	-6.0089297	\N	\N	12
860	Ferreteria_3	physical	27.9018013	-15.4466066	\N	\N	12
861	Würth_1	physical	43.4514614	-3.8352109	\N	https://www.wurth.es/	12
862	Solano	physical	37.1274306	-5.4504654	\N	\N	12
863	Suministros Valdepeñas	physical	38.7657677	-3.3874293	Avenida de Gregorio Prieto, 31, 13300, Valdepeñas	\N	12
864	La Llave_1	physical	38.7609449	-3.387322	Calle de las Escuelas, 57, 13300, Valdepeñas	\N	12
865	Almacenes Ferretería El Clavo SA	physical	38.7674408	-3.3878477	Avenida de Gregorio Prieto, 26, 13300, Valdepeñas	\N	12
866	Suministros Valdepeñas_1	physical	38.7680012	-3.3882501	Avenida de Gregorio Prieto, 35, 13300, Valdepeñas	\N	12
867	Ferreteria Amancio	physical	43.0756714	-8.4083778	\N	\N	12
868	Ferretería Reyes	physical	40.827642	-5.514686	\N	\N	12
869	SUMRRASSA	physical	41.5441175	2.0305499	\N	\N	12
870	VALPI	physical	41.5540086	2.026266	\N	\N	12
871	Comercial MHM	physical	40.827967	-5.513764	\N	\N	12
872	Comercial MHM_1	physical	40.8280489	-5.5136517	\N	\N	12
873	Solana	physical	40.3507916	-3.6958203	\N	\N	12
874	Ferreteria La Salut	physical	41.4426678	2.2257523	Passeig de la Salut, 105, 08914, Badalona	\N	12
875	Hardware Store	physical	40.8105959	0.511769	Tortosa	\N	12
876	Ferretería La Manilla	physical	42.236437	-8.7192375	Rúa Uruguai, 8, 36201, Vigo	\N	12
877	Ferreteria TB	physical	39.5023871	-0.4205979	Calle del Pintor Garnelo, 13, 46035	\N	12
878	Ferretería Yuste	physical	41.3971325	2.1813697	Carrer de Sardenya, 163-167, 08013, BARCELONA	\N	12
879	Ferretería Hermógenes Delgado Guerra	physical	28.384293	-16.6107849	\N	\N	12
880	Ferreteria Ferrowind	physical	36.1441462	-5.7004155	Facinas	\N	12
881	El Hogar	physical	43.290351	-2.9960057	\N	\N	12
882	Sistach	physical	42.1037347	1.8536438	\N	\N	12
883	Ferrobox	physical	40.1263368	-5.6601795	\N	\N	12
884	Ferretería Venecia	physical	40.4478002	-3.6685277	\N	\N	12
885	Ferretería Marino e Hijos SL	physical	40.3493931	-3.8024291	\N	\N	12
889	Ferretería La Llave Oscense	physical	42.1326569	-0.403006	\N	\N	12
890	Roberto Tapia	physical	28.0146591	-16.6527455	Avenida Fernando Salazar González, 9	\N	12
891	Almazán	physical	37.6383808	-3.6397331	\N	\N	12
892	Ferretería Coruñesa	physical	43.353737	-8.3971266	\N	\N	12
893	Garis	physical	41.6274684	-4.741786	\N	\N	12
923	Roycha_1	physical	42.3630116	-3.7515965	Calle Condado de Treviño, 4, 09001, Burgos	\N	12
924	La Campana	physical	38.2548238	-3.1313162	\N	\N	12
925	Torres_1	physical	38.25471	-3.1312625	\N	\N	12
926	Ferretería García	physical	38.0484743	-3.4620394	\N	\N	12
927	Electra San Cristóbal	physical	38.0475313	-3.4633468	\N	\N	12
928	Ferretería Arjonilla	physical	37.9770851	-4.1124236	\N	\N	12
929	Ferretería Maluco	physical	42.7767041	-7.4129901	\N	\N	12
930	Ferretería Fariña	physical	43.227182	-8.2884251	San Marcos, Abegondo	\N	12
931	Contaval automatismos y componentes electrónicos, S.L.	physical	41.3723545	2.1429068	Carrer de Sant Pere d'Abanto, 22, 08014, Barcelona	https://www.contaval.es/	12
932	Contaval automatismos y componentes electrónicos, S.L._1	physical	40.4329929	-3.6082298	Calle de María Sevilla Diago, 16	https://www.contaval.es/	12
933	Ferreteria Pedrola	physical	41.5116062	2.1914304	Plaça de Cirera Voltà	\N	12
934	Ferretería Jesús Gonzalez	physical	43.2278589	-8.3557162	\N	\N	12
935	Ferretería Sáez	physical	38.104432	-1.857068	\N	\N	12
936	Ferretería Las Parras	physical	37.5902309	-3.8181442	\N	\N	12
937	J. Salor	physical	43.3238957	-3.0296388	\N	\N	12
942	Ferretería Avenida_1	physical	40.2067911	-3.5786041	\N	\N	12
943	Taller Diba Bricolage	physical	40.4716738	-3.701486	Paseo de la Dirección, 366	\N	12
944	Ferretería Lauro Chichón	physical	40.4702685	-3.6919193	\N	\N	12
945	Ferretería Fidalgo	physical	40.46741	-3.6943048	Calle del Cañaveral, 27, 28029, Madrid	\N	12
946	La Hondura	physical	28.7300234	-13.8744554	\N	\N	12
947	Ferretería San Francisco	physical	41.0072944	-5.6475728	Calle San Francisco, 40, 37184, Villares de la Reina	\N	12
961	Ferretería Llamas	physical	41.3637046	2.0844571	Carrer de les Camèlies, 8, 08940, Cornellà de Llobregat	\N	12
962	Leroy Merlin_14	physical	37.1448937	-3.6131644	18100, Armilla	https://www.leroymerlin.es	12
963	Ferretería Beltrán	physical	39.4550225	-0.4623868	\N	\N	12
964	Torguesa Industrial, S.L.	physical	43.0487285	-7.5731426	\N	\N	12
965	Ferretería Anglés	physical	41.3623677	2.0809214	Carrer de la Buguenvíl·lea, 8, 08940, Cornellà de Llobregat	\N	12
966	Ferretería Isabel	physical	40.0542532	0.0625031	\N	\N	12
967	Suministros Martín	physical	42.7940815	-4.261409	\N	\N	12
968	Ferretería Los Pinos	physical	38.6553968	0.0777642	\N	\N	12
969	Ferretería Orotava	physical	28.3895027	-16.5250713	Calle Carrera del Escultor Estévez, 16, La Orotava	\N	12
970	Taller Hermános Fernández	physical	40.525165	-2.8279759	Paraje El Lavadero, Alhóndiga	\N	12
1017	Ferretería Ballesteros	physical	40.4316607	-3.7114064	\N	\N	12
1018	Ferretería Aguirre	physical	40.4625117	-3.6975644	Calle de Bravo Murillo, 305	\N	12
1019	becerra	physical	36.9317445	-4.5284582	\N	\N	12
1020	Aldana	physical	36.9297484	-4.5329402	\N	\N	12
941	Juan H. Rey	physical	43.4604086	-8.2564948	\N	\N	12
948	Leroy Merlin_13	physical	42.1708703	-8.6205928	\N	\N	12
949	Comercial Bugarín	physical	42.1482896	-8.6644243	Abelenda, 2, 36412, O Porriño	\N	12
950	Ferretería Areas	physical	43.2949703	-8.1271735	74	\N	12
951	Ferretería Fernandez	physical	43.65608	-7.5990089	\N	\N	12
952	Ferretería Luis	physical	43.659937	-7.5962992	\N	\N	12
953	Optimus_1	physical	38.6460472	0.0401922	\N	https://www.optimusferreteria.com/	12
954	Ferretería La Escalera	physical	40.4660456	-3.719837	\N	\N	12
955	Meedeira Carpintería	physical	43.2214567	-8.3581473	\N	\N	12
956	L'eina aixerida	physical	41.5818066	2.0129406	\N	\N	12
957	Iparsat Telecomunicaciones, S.L.	physical	43.3107476	-1.9120174	Aita Donostia kalea, 20100, Errenteria	https://www.iparsat.com/	12
958	Ferretería Leganés	physical	40.327171	-3.7633295	\N	\N	12
959	Fergo	physical	40.3266315	-3.7627046	\N	\N	12
960	Roque	physical	43.2770851	-8.2128468	\N	\N	12
971	Ferrateria Puig	physical	42.0410436	3.1240198	\N	\N	12
972	Les parisines	physical	42.041894	3.1269982	\N	\N	12
973	El Martillo	physical	40.0749213	-2.1368676	\N	\N	12
974	Azulejos Peña_1	physical	40.4860636	-3.6845463	\N	\N	12
975	La del Manojo	physical	40.3532033	-3.698435	\N	\N	12
976	Ferreteria Silvano	physical	40.4625018	-3.6300384	\N	\N	12
977	Las Torres	physical	37.1885139	-3.6193917	\N	\N	12
978	Electromoba	physical	37.8802807	-4.7671168	Calle Escritor Sebastián Cuevas, 1	https://electromoba.es	12
979	Caramés	physical	42.8656511	-8.6783456	Avenida de Santa Minia, 15865, Pedrouzos	\N	12
980	Venecia_2	physical	40.4348068	-3.7041313	\N	\N	12
981	Ferretería Ruvira	physical	37.7451885	-0.9536728	\N	\N	12
982	Ferretería Fernández_1	physical	37.7439053	-0.9531847	\N	\N	12
983	Kisi	physical	43.2957694	-2.9908745	\N	\N	12
984	Ferretería Alonso_3	physical	40.4244611	-3.5633369	\N	\N	12
985	Ferretería El Paseo	physical	37.8933209	-6.5618378	Calle Rosal	\N	12
986	Ferretería La Tabacalera	physical	37.8941258	-6.5607259	Plaza Marqués de Aracena	\N	12
987	Ferreteria Xaloc	physical	41.3744184	2.162718	Blai, 52	\N	12
988	Electrobrico Garden	physical	37.8976175	-6.5689386	\N	\N	12
989	Ferretería Modesto	physical	40.0892997	-6.3524972	\N	\N	12
990	Ferreteria Manresana	physical	41.730183	1.817981	Avinguda de Tudela, 11-15	\N	12
991	Ferreteria de la Muñoza, S.C.P.	physical	41.5461036	2.2065919	Avinguda de Rivoli, 15-17	\N	12
992	Util Bages, S.L.	physical	41.7269637	1.8401503	Carrer de Viladordis, 101	\N	12
993	Vazquez Gabalda S.C.P.	physical	41.4578686	2.0649243	\N	\N	12
994	Ferreteria la Sariera	physical	38.9189541	-0.1180747	Carrer Major, 46780, Oliva	\N	12
995	Beltrán	physical	39.9813405	-0.0496258	\N	\N	12
996	Desatascos Castellon	physical	39.9813174	-0.0470355	\N	\N	12
997	Sierra	physical	43.5875205	-5.7687243	\N	\N	12
998	Ferretería Aracena	physical	37.8881289	-6.5569953	\N	\N	12
999	Ferretería FerreHogar	physical	37.7797568	-3.7876169	Calle Miguel Castillejo, 2, 23008, Jaén	https://ferreteriaferrehogar.negocio.site/	12
1000	Ferretería Bricolaje	physical	37.9076658	-0.8526706	\N	\N	12
1001	El Arca de Noé	physical	37.3785997	-6.0055897	\N	\N	12
1002	Ferrobox Herramentas	physical	38.1938958	-0.5725241	\N	\N	12
1003	Hermanos Guerrero	physical	37.7441705	-0.9572991	\N	\N	12
1004	Aleu	physical	36.4654128	-6.1985127	\N	\N	12
1005	Manualidades El Dintel	physical	36.4612765	-6.2043071	\N	\N	12
1006	Toy Soldier Maquetas	physical	36.4663892	-6.1968756	Calle del General García de la Herrán, 11100, San Fernando	\N	12
1007	Suministros Americanos	physical	36.4664376	-6.1973409	\N	\N	12
1008	Ferretería Martínez	physical	37.1900761	-3.609119	\N	\N	12
1009	Comercial Youremar	physical	28.0829772	-17.333633	\N	\N	12
1010	Naturavia Casas prefabricadas y alquiler de caravanas	physical	40.5675633	-3.603535	Carretera de Burgos, km. 20.800	http://www.gruponaturavia.com	12
1011	Jarama Casas prefabricadas y Caravanas	physical	40.5743248	-3.5951203	Carretera de Burgos, Km 22, 28703, San Sebastian De Los Reyes	https://casasmovilesjarama.com/	12
1012	Leroy Merlin_15	physical	41.7232162	1.8481964	Carrer d'Agustí Coll, 2, 08243, Manresa	\N	12
1013	Ferreteria el Barato	physical	41.9127489	1.6813645	\N	\N	12
1014	Nautica Herreson,s.l.	physical	38.2175388	-0.5939549	\N	\N	12
1015	Materiales Cano	physical	38.2184902	-0.6842047	\N	\N	12
1016	Palerm	physical	39.7705715	3.1429389	\N	\N	12
1027	Ferreteria San Martín	physical	43.3139143	-1.9388354	\N	\N	12
1028	Barchafe_2	physical	37.7735025	-3.7932741	\N	\N	12
1043	Ferretería Úceda	physical	40.4727792	-3.3700316	\N	\N	12
1044	A. Morales	physical	36.419156	-6.1476471	\N	\N	12
1045	Merca Lifeng	physical	27.7594412	-15.6817277	Calle Miguel Marrero Rodríguez, 53, Arguineguin	\N	12
1046	Solingen Paris Barcelona	physical	41.3824504	2.1739136	\N	\N	12
1053	Cusal	physical	41.2351093	1.7342876	Rambla dels Països Catalans, 18, 08800	\N	12
1054	Cuchilleria Fernandez	physical	38.9664677	-0.1816554	\N	\N	12
1055	La Tienda de la Personalización	physical	40.4730491	-3.7118147	\N	\N	12
1065	Ferretería El Metro	physical	28.1078994	-15.4186021	\N	\N	12
1066	La Cabaña del bricolaje	physical	41.6383201	-0.8782067	\N	\N	12
1067	Repuestos y accesorios de electrodomésticos	physical	41.6363241	-0.8749346	\N	\N	12
1068	Ferretería Comercial Artigas	physical	41.6387911	-0.8798127	\N	\N	12
1069	Ferretería Benito	physical	40.4826979	-2.7320393	\N	\N	12
1070	Ceramistas	physical	28.1062601	-15.4191916	\N	\N	12
1071	Chasbel	physical	41.6467356	-0.8906995	\N	\N	12
1072	Comercial Jayca	physical	41.6463817	-0.8896918	\N	\N	12
1073	Ferreteria el Candao	physical	39.4159043	-0.7874415	\N	\N	12
1074	PLA-IBER S.a.	physical	41.9434029	2.7817418	\N	\N	12
1075	Ferreteria de Sineu	physical	39.6436366	3.0074029	\N	\N	12
1076	DSf Ferreters	physical	42.4161538	1.1320748	\N	\N	12
1077	Ferretería Mercadal	physical	41.667095	-0.833007	Avenida de Santa Isabel, 70, 50016, Zaragoza	\N	12
1078	Bricocassals	physical	41.0773097	1.1814211	Passeig de Pau Casals	\N	12
1079	Llompart	physical	39.4897737	2.8908683	\N	\N	12
1080	Ferretería Aries	physical	41.6498787	-0.8990317	\N	\N	12
1081	Ferretería Casa Rivas	physical	41.7404906	-6.2741112	\N	\N	12
1082	Max Mak Hiperhogar	physical	41.6591804	-0.9183982	\N	\N	12
1083	Honda maquinaria Sampietro	physical	41.6551326	-0.9061705	\N	\N	12
1960	Brico_1	physical	42.3484724	-3.7138275	\N	\N	12
1021	Ferretería Encarna	physical	38.0369592	-1.4913554	\N	\N	12
1022	Ferreteria Rosaplata	physical	36.4957867	-4.7792892	\N	https://www.ferreteriarosaplata.com/	12
1023	Ferreteria Sales	physical	41.2387426	1.8109906	Avinguda de l'Hort Gran, 12, 08870, Sitges	\N	12
1024	Ferretería Viver	physical	39.9206413	-0.5962387	\N	\N	12
1025	el Palau	physical	39.572063	3.1823919	\N	\N	12
1026	BricoDepot Vitoria	physical	42.9113594	-2.717456	\N	\N	12
1029	impresoras3d.com	physical	36.8415552	-2.4571052	Carrera del Duende, 12, 04005, Almería	https://www.impresoras3d.com	12
1030	Ferretería El Burgo	physical	41.5866308	-3.0663803	\N	\N	12
1031	Ferretería Mallón	physical	43.159171	-8.8054471	Rúa Manuel Abelenda, 15148, Coristanco	\N	12
1032	Novasur - Maquinaria suministros industriales	physical	42.290463	-7.8354947	\N	\N	12
1033	Leroy Merlin Exprés Prosperidad	physical	40.4443446	-3.673692	Calle de López de Hoyos, 120, 28002, Madrid	https://www.leroymerlin.es/tiendas/expres-prosperidad.html	12
1034	La Inmaculada	physical	40.3250136	-3.7711467	\N	\N	12
1035	Stihl - Suministros Yesca, S.L.	physical	42.9456894	-3.4823921	\N	\N	12
1036	El Hórreo_1	physical	42.8761214	-8.5441099	Rúa do Hórreo, 22, 15701, Santiago de Compostela	\N	12
1037	marquez	physical	42.8206484	-1.6691047	\N	\N	12
1038	Ferretería Cancho_2	physical	39.4857426	-6.3641727	\N	\N	12
1039	Ferretería La Unión	physical	36.3701106	-6.180158	Carretera de la Barrosa, 11139	\N	12
1040	Ferretería Rodríguez Arciniega	physical	41.670473	-3.688577	Calle Béjar, 1	\N	12
1041	Francisco Dinnbier	physical	39.4748109	-0.3885804	\N	\N	12
1042	Ferretería Chamartín	physical	40.4644461	-3.6948567	Calle de Bravo Murillo, 336, 28020, Madrid	\N	12
1047	Can Boira	physical	39.6919475	3.3450232	\N	\N	12
1048	BRICO DEPOT	physical	36.8740152	-2.4486983	\N	\N	12
1049	Venecia_3	physical	40.4347971	-3.7037008	\N	\N	12
1050	Bricordino	physical	28.105237	-15.4151899	\N	\N	12
1051	Clickfer Galán	physical	43.0224611	-7.5645852	\N	\N	12
1052	Leroy Merlin_16	physical	43.3434588	-8.4284753	Estrada dos Baños de Arteixo, 43, 15008, A Coruña	https://www.leroymerlin.es/	12
1056	sars	physical	41.4608885	2.2520805	Carrer de l'Energia, 25, 08915	\N	12
1057	Sobrinos	physical	42.3471041	-3.6506976	\N	\N	12
1058	Suministros Viper	physical	42.3470642	-3.6489366	Calle Alcalde Martín Cobos, 09001, Burgos	\N	12
1059	Ferretería La Ventilla	physical	40.468674	-3.6933454	\N	\N	12
1060	Alabaz II	physical	39.4568265	-0.3905409	Fontanares, 4	\N	12
1061	Ferretería Paco	physical	38.1466856	-0.6451623	\N	\N	12
1062	Ferrymas	physical	41.6452894	-0.8895508	\N	\N	12
1063	Ferreteria_4	physical	40.2102326	-3.5716888	\N	\N	12
1064	OK Soluciones	physical	37.6096778	-0.9882066	Avenida Reina Victoria Eugenia, 30, Cartagena	\N	12
1109	La Extremeña	physical	39.9852325	-6.5345328	\N	\N	12
1110	Ferretería Pérez Rey	physical	43.1386197	-9.1189007	Rúa do Porto, 15121, A Ponte do Porto	\N	12
1111	Maquinaria de jardinería y construcción	physical	40.5776504	-3.9300315	\N	\N	12
1112	Amado Cárdenes, Maquianaria de Hostelería_1	physical	28.1097431	-15.4174422	\N	\N	12
1113	Amado Cárdenes, Maquianaria de Hostelería_2	physical	28.1099762	-15.4169194	\N	\N	12
1114	Ferretería Sebastián Pérez e hijos	physical	37.7960074	-7.1927352	Avenida de Portugal, 33, 21570, Santa Bárbara de Casa	\N	12
1117	Optimus_2	physical	28.9729615	-13.564081	\N	\N	12
1118	Tucerel	physical	41.6426215	-0.8883244	\N	\N	12
1119	Ferretería F. Del Campo	physical	40.5608732	-3.612865	Calle María Moliner, 7, 28703, San Sebastián de los Reyes	https://ferreteriafdelcampo.es	12
1120	Aislamientos Moncayo	physical	41.6556467	-0.90247	\N	\N	12
1121	Buzones Aragón	physical	41.6550114	-0.9013462	\N	\N	12
1122	Ferretería Valdepasillas	physical	38.8707326	-6.9897277	\N	\N	12
1123	Ferretería Calvo	physical	41.6473772	-0.8741937	\N	\N	12
1124	Ferretería Rex	physical	41.6623266	-0.8642578	\N	\N	12
1125	Ferretería Méndez 2	physical	41.3402796	2.0440729	Carrer de la Indústria, 22	\N	12
1126	Ferretería Bufalà	physical	41.4584762	2.2430308	\N	\N	12
1127	Recambios Urra	physical	43.341439	-1.7978956	\N	\N	12
1128	Fag, Estanterías Metálicas	physical	28.1158141	-15.4262957	\N	\N	12
1129	Farfisa, Videoporteros	physical	28.1155935	-15.4267906	\N	\N	12
1130	Hogar Color	physical	28.1134132	-15.4252443	\N	\N	12
1131	Impelcasa, Importaciones eléctricas	physical	28.1160357	-15.4268444	\N	\N	12
1132	J. Fdez. Romero, Fleck	physical	28.1155822	-15.4261598	\N	\N	12
1133	Tubalca	physical	28.1138644	-15.4273368	\N	\N	12
1134	Yuba	physical	28.1136654	-15.4259572	\N	\N	12
1135	Ferretería Toledo	physical	28.1154262	-15.4253481	\N	\N	12
1136	Cerrajería Gorayeb	physical	28.1145933	-15.4230482	\N	\N	12
1137	Comercial Jupama, Máquinas Recreativas	physical	28.1152526	-15.4240205	\N	\N	12
1138	Yesos Rubio	physical	28.1166826	-15.423222	\N	\N	12
1139	7 Islas, Pintura	physical	28.1168183	-15.4232861	\N	\N	12
1140	Bayon Maquinaria	physical	28.1145938	-15.4207131	\N	\N	12
1141	Fichet, cajas fuertes	physical	28.1158452	-15.4220292	\N	\N	12
1142	7 Islas, Pintura_1	physical	28.1169828	-15.4230301	\N	\N	12
1143	Tornillera Aragonesa	physical	41.6614272	-0.8643134	\N	\N	12
1144	Ferretería Efrain	physical	42.9371977	-3.4848831	\N	\N	12
1145	Fissel	physical	38.2403915	-6.0146958	Avenida Jesús de Nazaret, 31	\N	12
1146	Ferrymas_1	physical	41.6520856	-0.9098091	\N	\N	12
1167	Ferretería Suiza	physical	39.6626769	-0.2296583	\N	\N	12
1168	Ferretería El Port	physical	39.6668482	-0.2333262	\N	\N	12
1169	Ferretería Induhogar	physical	42.5210769	-0.3602931	Calle del Serrablo, 134, 22600, Sabiñánigo	\N	12
1170	Ferreteria Calatorao	physical	41.525055	-1.3462214	Calle Poeta Pedro Marcuello, 6, Calatorao	\N	12
1171	Roycha_2	physical	42.3450286	-3.6894671	Calle Briviesca, 34, 09004, Burgos	www.casataller.es	12
1172	Sánchez Gozalo	physical	42.3362505	-3.7027531	\N	\N	12
1173	San Antolín	physical	40.3894741	-3.6474895	\N	\N	12
1174	talleres Sepulcre	physical	38.2531377	-0.7042683	\N	\N	12
1175	Hijos de CV Otero	physical	42.911545	-8.5148352	\N	https://www.hcvotero.es/	12
1176	Recambios Santiagueses S. L.	physical	42.9098665	-8.5209696	Rúa de María de los Ángeles de la Gándara, Naves 5 y 7, 15890	http://www.santiagueses.com	12
1177	Ferretería Sánchez_2	physical	36.8436366	-2.4470517	04006	\N	12
1178	Leroy Merlin_17	physical	41.3873539	2.0400466	Carretera de Laureà Miró, 361, 08980, Sant Feliu de Llobregat	\N	12
1084	Amado Cárdenes, Maquianaria de Hostelería	physical	28.1097076	-15.4170472	\N	\N	12
1085	Ferretería Colmenares	physical	28.1094869	-15.4173106	\N	\N	12
1086	Ferretería Venegas	physical	28.110557	-15.417439	\N	\N	12
1087	RistorM@rkt, Maquinaria de Hostelería	physical	28.1095852	-15.41732	\N	\N	12
1088	Bricolage Madera	physical	28.1133117	-15.4235171	\N	\N	12
1089	Cerrajería La Clave	physical	28.1130103	-15.4231262	\N	\N	12
1090	Arquinsa	physical	41.6793081	-0.9560524	\N	\N	12
1091	Artecma Carretillas	physical	41.6785591	-0.9581635	Calle Zuera, 14	\N	12
1092	Autoservicio ventas Fontasa	physical	41.6779804	-0.9592395	Calle Zuera	\N	12
1093	Avenmar	physical	41.6791094	-0.9557045	Calle Zuera, 24	\N	12
1094	Copes	physical	41.6784237	-0.9583068	\N	\N	12
1095	Fontasa	physical	41.6781201	-0.9575641	\N	\N	12
1096	Ilunor	physical	41.6779978	-0.9587834	\N	\N	12
1097	Matilsa Alquiler de herramientas	physical	41.6814657	-0.9630903	\N	\N	12
1098	Orcal	physical	41.6778603	-0.958953	Calle Zuera, 4	\N	12
1099	Productor Imán	physical	41.6787884	-0.9583448	\N	\N	12
1100	Promoaral	physical	41.6786705	-0.9584676	\N	\N	12
1101	Sedag	physical	41.6794741	-0.9571986	\N	\N	12
1102	Uneted	physical	41.6800441	-0.9570232	Calle Zuera, 23	\N	12
1103	Ferretería ROS	physical	38.0057922	-1.0707763	\N	\N	12
1104	Ferreteria Torremendo	physical	37.9919842	-0.8672697	\N	\N	12
1105	Ferretería Crismmar	physical	28.1111089	-15.4218117	\N	\N	12
1106	AKÍ	physical	40.0070806	-6.1114169	\N	\N	12
1107	AKI	physical	40.0064765	-6.1104185	\N	\N	12
1108	Ferreteria_5	physical	38.013852	-1.0353262	\N	\N	12
1115	Cuchillería Martínez	physical	41.6531051	-0.9022371	\N	\N	12
1116	Maspor	physical	41.6639744	2.2669537	\N	\N	12
1147	La Herramienta Salmantina	physical	40.9759031	-5.6487728	\N	\N	12
1148	Ferretería_9	physical	41.0703803	1.1508825	Carrer de Falset, 27, 43840	\N	12
1149	Puig	physical	41.5120178	2.1348789	\N	\N	12
1150	Aki	physical	40.5322061	-3.644242	\N	\N	12
1151	Decofer	physical	42.6972844	-6.5151401	\N	\N	12
1152	Royán	physical	38.1930801	-0.5824462	\N	\N	12
1153	Ferreteria Armand	physical	41.8646701	1.8746137	\N	\N	12
1154	Bricolaje Pinillos	physical	39.6606651	-0.2162294	\N	\N	12
1155	J. Díaz grupos electrógenos y compresores	physical	39.6621202	-0.2165909	\N	\N	12
1156	viking	physical	38.3823645	-0.7645816	c/Almoina, 35	\N	12
1157	BigMat	physical	38.4522213	-2.0490092	\N	\N	12
1158	El Talabartero	physical	38.451273	-2.048596	\N	\N	12
1159	Tr Distribuciones Industriales	physical	41.2438352	1.7219035	Camí Ral de la Masia Cabanyes, 2, 08800	\N	12
1160	Diadal	physical	43.5311817	-5.6722264	Gijón/Xixón	\N	12
1161	González	physical	40.5978695	-6.5339532	\N	\N	12
1162	Diher SA	physical	40.4360545	-3.7032651	\N	\N	12
1163	Dilo	physical	43.1874288	-8.7351948	\N	\N	12
1164	Husqvarna	physical	43.1885337	-8.7347442	\N	\N	12
1165	Casa Cerdanyola	physical	41.4929978	2.142372	\N	\N	12
1166	Basar Oriental	physical	41.4933214	2.1436184	\N	\N	12
1187	Almericentro	physical	36.8370935	-2.4619004	\N	\N	12
1188	Ferretería El Llavín	physical	36.7402843	-4.0963401	\N	\N	12
1189	Daikin Klimacentro	physical	36.744358	-4.0886425	\N	\N	12
1190	Hermanos Jeromo S.A,	physical	36.7843792	-4.1121836	\N	\N	12
1191	Sergio Sarmiento-Garden Tools	physical	36.7826118	-4.1089904	\N	\N	12
1193	Ferreteria Moll Menorca SL	physical	40.0056676	3.8482471	Carrer de Nostra Senyora de la Consolació, 18, 07760, Ciutadella deMenorca	https://ferreteria-moll.com/	12
1194	Fidel Martín	physical	36.763822	-4.0949119	\N	\N	12
1195	Yedesa	physical	36.7357313	-4.1071303	\N	\N	12
1196	Ferreteria Ferronaval	physical	28.1490518	-15.4294677	Calle Luján Pérez, 8	\N	12
1197	Angelo	physical	43.5301687	-5.6671234	\N	\N	12
1198	García Sanjaime	physical	39.4602516	-0.3340744	\N	https://www.sanjaime.es/	12
1199	Ferrhogar	physical	41.4173045	2.1976799	\N	\N	12
1200	Lamagrande_1	physical	40.4380958	-3.6535919	\N	\N	12
1201	Ferreteria Valls	physical	41.3796118	2.161666	\N	\N	12
1202	Ferreteria Sant Antoni	physical	41.3798175	2.1634301	Ronda de Sant Antoni, 24	\N	12
1203	Fontelec	physical	42.1211271	2.7842876	Carrer de Puigpalter	\N	12
1204	América	physical	40.4388494	-3.6736337	\N	\N	12
1205	Berner	physical	40.4352584	-3.532927	\N	\N	12
1206	Ferreteria Farran	physical	41.3757424	2.1682298	\N	\N	12
1207	Fontanería Granda	physical	40.4376805	-3.653028	\N	\N	12
1213	Ferreteria Torrebadella.	physical	41.8991993	1.8771117	\N	\N	12
1214	Rafael Y Daniel	physical	36.7342671	-4.1738535	\N	\N	12
1215	Nueva Ferretería_1	physical	40.4286572	-3.669609	\N	\N	12
1216	La Clau_1	physical	41.9950077	1.5220246	\N	\N	12
1217	Luiso	physical	40.4351387	-3.6586696	\N	\N	12
1218	Ferrokey	physical	40.4322122	-3.6557556	\N	\N	12
1219	Piscinas Mediterráneo	physical	36.7446148	-4.0890586	\N	\N	12
1220	Azuleos Diseno	physical	36.745348	-4.0877731	\N	\N	12
1221	Cristaleria Xavier	physical	41.6230269	0.6185278	\N	\N	12
1222	100 Idees	physical	41.6218694	0.6195604	Carrer dels Amics de Lleida, 10, 25008	\N	12
1223	Tancaments T-Quattre	physical	41.6212837	0.6217433	Carrer d'Humbert Torres, 6, 25008	\N	12
1224	Venecia_4	physical	40.4370986	-3.6528671	\N	\N	12
1225	La Mirandesa materiales de construcción	physical	40.4695744	-3.706905	\N	\N	12
1226	Onsa	physical	40.4408525	-3.6429566	\N	\N	12
1227	Comercial Metabos_1	physical	40.9913398	-5.6432732	Calzada de Toro, 28	http://www.metabos.com/	12
1228	Hidro Tarraco	physical	41.6288053	0.6236318	Carrer del Penedès, 89, 25005, Lleida	\N	12
1229	J. Pelegrí	physical	41.623266	0.6182755	Carrer de Sant Hilari, 25008	\N	12
1230	Ferretería Saconia	physical	40.4684432	-3.7225408	\N	\N	12
1251	BigMat Mercamat	physical	41.8969611	3.1442705	\N	\N	12
1252	Iresa	physical	41.6139147	0.6810338	Carrer M	\N	12
1253	Ferreteria Ramon Soler - Optimus	physical	41.613	0.6777439	Polígon Industrial Camí dels Frares, Carrer J, 25190, Lleida	https://www.ramonsoler.com/	12
1254	Ferretería Ferroca	physical	39.1072516	-6.6889803	\N	\N	12
1257	Ferretería Femag saneamiento	physical	40.4382246	-3.6361576	\N	\N	12
1258	Ferretería Del Pozo	physical	43.2566532	-2.9255431	\N	\N	12
1259	Evimar	physical	42.6850676	-2.9433408	\N	\N	12
1260	Ferretería Expeleta	physical	43.2622554	-2.925301	Bilbao	\N	12
1261	Nebreda	physical	42.6880655	-2.9437852	\N	\N	12
1283	Alvemar	physical	42.0384742	3.1341246	\N	\N	12
1179	Keraben sanitarios	physical	42.3585825	-3.6519965	\N	\N	12
1180	Grupo Copsa	physical	42.358495	-3.6523062	\N	\N	12
1181	El Comercio	physical	41.1344533	-3.688447	\N	\N	12
1182	Suc. José Cal Gato	physical	43.6686855	-7.6043375	\N	\N	12
1183	Ferretería Plácido	physical	43.6714463	-7.6113944	\N	\N	12
1184	Ferretería Dial	physical	36.8382618	-2.450888	\N	\N	12
1185	El Martillo_1	physical	36.837157	-2.4580336	\N	\N	12
1186	JAMA	physical	36.8354043	-2.4589965	\N	\N	12
1192	Pintures Vic	physical	41.7353808	1.8396948	Carrer de Sallent	http://www.pinturesvic.com	12
1208	Ferreteria El Faro	physical	41.6238939	0.6211638	Gran Passeig de Ronda, 154, 25008, Lleida	http://www.ferreteria-elfaro.com/	12
1209	El Metro	physical	41.6252143	0.6242967	\N	\N	12
1210	Ferretería Daluz	physical	36.7311714	-4.1305903	\N	\N	12
1211	Suministros Agrícolas Coca	physical	36.7306216	-4.128824	\N	\N	12
1212	Hnos Perez Cocinas	physical	36.7333697	-4.1369322	\N	\N	12
1231	Rodamientos Duero	physical	41.6720506	-3.7071773	Avenida del Montecillo, P24 - Nave 6, 09400, Aranda de Duero	\N	12
1232	Ferretería Dase	physical	38.0618061	-6.6468964	\N	\N	12
1233	Delsan	physical	43.2479682	-2.9303645	\N	\N	12
1234	Ferretería Yago	physical	41.6498215	-0.9143504	Calle de Mosén Andrés Vicente, 16, 50017	https://www.ferreteriayago.com/	12
1235	Ferretería La Purísima	physical	36.7478152	-3.0136004	Calle Velázquez, 18, 04770	\N	12
1236	Ferreteria Olle	physical	41.376882	1.1620355	\N	\N	12
1237	Ferretería Mollet	physical	41.5407298	2.2092857	Rambla Nova, 79	\N	12
1238	La labradora	physical	38.9951341	-1.8593462	\N	\N	12
1239	Ferretería J. Calles	physical	41.0081872	-6.4351746	Plaza de España, 7, 37210, Vitigudino	\N	12
1240	Riosmat BigMat	physical	41.0086262	-6.4357071	Calle de San Juan de Dios, 1, 37210, Vitigudino	https://www.riosmat.bigmat.es/	12
1241	Goes	physical	40.2337255	-4.3897967	\N	\N	12
1242	Ferretería Blázquez	physical	40.4275879	-3.7188452	Calle de Ferraz, 25, 28008, Madrid	\N	12
1243	Oltivas	physical	40.4365572	-3.6725711	\N	\N	12
1244	HiperTecno	physical	40.4360872	-3.7026971	\N	\N	12
1245	BigMat_1	physical	36.2805415	-6.0895224	\N	\N	12
1246	Sual	physical	39.1543703	-0.4303803	Carrer de l'Ardiacà Pere Esplugues, 77, 46600, Alzira	\N	12
1247	Riosmat BigMat_1	physical	41.0089984	-6.4387296	\N	https://www.riosmat.bigmat.es/	12
1248	Brico	physical	42.3484194	-3.7142005	\N	https://www.brico-burgos.es/	12
1249	Polet	physical	43.3176564	-1.9184912	\N	\N	12
1250	Ferretería Qin Qin	physical	38.4729509	-0.7984874	\N	\N	12
1255	Nervión	physical	43.2557857	-2.9237262	\N	\N	12
1256	Ferretería Ayala	physical	40.4267594	-3.6671868	\N	\N	12
1262	Bricolaje Tubía	physical	42.6893905	-2.9415621	\N	\N	12
1263	Medina	physical	42.6874333	-2.9387388	\N	\N	12
1264	Ferreteria Motxilla	physical	41.4966626	0.4614212	\N	\N	12
1265	Papelhogar	physical	40.4100066	-3.7104371	Calle del Humilladero, 20, 28005, Madrid	\N	12
1266	Valvulería Medrano	physical	42.6858884	-2.9357242	\N	\N	12
1267	Tekocerblan Suministros	physical	42.688508	-2.9385737	\N	\N	12
1268	Comercial Garcia	physical	36.9017384	-4.3422809	\N	\N	12
1269	Ferretería Pumarín	physical	43.3691855	-5.8437676	\N	\N	12
1270	Ferretería EL HOGAR	physical	43.2605473	-2.9337712	\N	https://elhogar.net/	12
1271	Optimus_3	physical	39.6027668	3.3827544	\N	\N	12
1272	Cadiñanos	physical	42.6844927	-2.9488573	\N	\N	12
1273	Urbiztondo	physical	42.6846366	-2.949139	\N	\N	12
1274	Suministros Centermant	physical	42.6846766	-2.9508088	\N	\N	12
1275	La Bolsa	physical	43.2631509	-2.9302028	\N	\N	12
1276	Repuestos López	physical	42.6871668	-2.9523285	\N	\N	12
1277	ALAN Establecimientos Industriales	physical	43.2663929	-2.9352811	\N	\N	12
1278	Ferreteria Abando_1	physical	43.2650185	-2.9309166	\N	\N	12
1279	Paher	physical	42.6923854	-2.9467946	\N	\N	12
1280	Ferretería Quintanar	physical	39.3479452	-1.9305333	\N	\N	12
1281	Ferretería El Globo	physical	39.4737261	-0.3799619	46001	\N	12
1282	Ferretería Ferpoli	physical	40.4345226	-3.8110729	Calle Nuestra Señora de la Consolación, 9, 28223	\N	12
1299	Bricolaje Delicias	physical	41.6482171	-0.9163982	\N	\N	12
1300	JUFEMA	physical	41.0076361	-6.4355805	Calle Santa Ana, 8, 37210, Vitigudino	\N	12
1301	Conesa	physical	37.9775429	-0.689247	Calle Villa de Madrid, 1, 03181, Torrevieja	\N	12
1302	Roymar Hispanidad	physical	41.6435066	-0.9120059	Calle de las Escuelas Pías, 2, 50009, Zaragoza	https://www.roymar.es/	12
1303	Herminio García Notario	physical	41.0075227	-6.4332285	Calle del Matadero, 2, 37210, Vitigudino	\N	12
1304	Ferretería José Luis Tapias Carrascal	physical	41.597804	-4.1192786	Calle de La Pedraja, 14, 47300, Peñafiel	\N	12
1305	Ferretería Valero	physical	36.7329272	-4.4154475	Calle Cristo de la Epidemia, 98, 29013, Málaga	\N	12
1306	Ferretería J. Calles_1	physical	41.0082118	-6.4349183	Calle Honda, 4, 37210, Vitigudino	\N	12
1307	Sáenz	physical	36.7325247	-4.4165334	Alameda Capuchinos, 84, Málaga	\N	12
1308	Bricentro	physical	36.7314696	-4.3968337	Avenida del Mayorazgo, 22, 29016, Málaga	\N	12
1309	BriCor_2	physical	40.4301735	-3.7161342	\N	\N	12
1310	Maprise	physical	43.2976257	-5.6846008	\N	\N	12
1325	Ferretería Fabian	physical	38.7938906	0.0335038	\N	\N	12
1326	Sagu	physical	42.3380397	-4.6025105	\N	\N	12
1327	Materiales de Construcción Casleón SL	physical	42.3373244	-4.5994927	\N	\N	12
1328	Casa Severón	physical	43.5390728	-6.7241184	\N	\N	12
1329	sant Miquel	physical	39.7199914	2.9167914	\N	\N	12
1330	Trabajo Seguro. Protección Laboral	physical	40.9641576	-5.651807	Camino Estrecho de la Aldehuela, 12, 37003, Salamanca	http://www.trabajo-seguro.com	12
1331	Juanma	physical	42.002642	-4.5259262	\N	\N	12
1332	Cada Millán	physical	41.8774726	-4.5456879	\N	\N	12
1333	Ferretería del Centro	physical	42.0047576	-4.5300464	\N	\N	12
1334	Comercial Fernández	physical	42.577289	-6.6637883	\N	\N	12
1335	Ferretería José	physical	42.5810892	-6.6723121	\N	\N	12
1336	Pinturas Toledano	physical	36.8440453	-2.4470537	\N	\N	12
1337	Casa Serafín	physical	42.6068744	-6.8087776	\N	\N	12
1338	Ferretería Bazar	physical	42.6073064	-6.8087583	\N	\N	12
1339	Ferretería Delgado_1	physical	40.4892538	-3.3574519	Calle Juan de Borgoña, 4	\N	12
1340	Santa Mariña	physical	43.4952466	-8.2267035	\N	\N	12
1341	Ferretería Olmos	physical	37.9784381	-1.1055596	\N	\N	12
1342	Zamudio	physical	43.2821285	-2.863432	\N	\N	12
1285	Ferreteria Herdisa	physical	43.2632225	-2.938018	\N	http://ferreteriaherdisa.com/Herdisa/cerrajeria.html	12
1286	Zarapool	physical	41.5946583	-0.9403486	72A	\N	12
1287	Hammerbox	physical	41.5948326	-0.940243	\N	\N	12
1288	Azulejos Pedraza	physical	40.4798687	-3.7158099	\N	\N	12
1289	Martin	physical	36.7504885	-3.8756448	\N	\N	12
1290	Gelabert	physical	39.5888704	2.6807496	\N	\N	12
1291	ABC Sant Boi	physical	41.3386967	2.0429276	\N	\N	12
1292	Ferretería Cantalapiedra	physical	43.2944445	-5.6841879	\N	\N	12
1293	La Leonesa	physical	40.446739	-3.8033631	Avenida de Juan Pablo II, 16, 28224	https://ferreterialeonesa.com/	12
1294	Ferralla Montesalgueiro	physical	43.2153638	-8.0650354	\N	\N	12
1295	BriCor_1	physical	39.4848506	-0.3973197	Avinguda de Pius XII, 51, 46015	http://bricor.es	12
1296	Ferretería Universitas	physical	41.6436598	-0.9098436	\N	\N	12
1297	Can Ros cadena 88	physical	39.4370083	3.0053947	\N	\N	12
1298	Marmoles Gallego	physical	42.3351304	-7.8593261	\N	\N	12
1311	La Panera	physical	43.4087032	-6.261107	\N	\N	12
1312	Taller de Afilados	physical	41.6556573	-4.7232126	\N	\N	12
1313	Ciudad&Cash	physical	41.4413687	2.1825458	Carrer del Vinyar, 20, 08016, Barcelona	\N	12
1314	BricoAlmonte	physical	28.522232	-16.3398455	\N	\N	12
1315	Ferragens	physical	36.7214003	-4.403322	Paseo de Sancha, 18, 29016, Málaga	\N	12
1316	Luces LED	physical	39.4694045	-0.3886635	\N	\N	12
1317	Alberto y Javier	physical	39.4692136	-0.3902656	\N	\N	12
1318	Ferreteria Optimus	physical	42.4332945	1.9221018	\N	\N	12
1319	Ferreteria "Los Molinos"	physical	27.762621	-15.5779678	\N	\N	12
1320	Obramat	physical	43.3915067	-5.7955134	\N	https://www.bricomart.es	12
1321	Ferretería Coia	physical	42.2180886	-8.7432736	\N	\N	12
1322	Ferretería Pelícano	physical	41.6466898	-4.7096634	Calle del Pelícano, 6, 47012, Valladolid	https://ferreteriapelicano.es/	12
1323	Ferreteria Pie De Rey	physical	42.1889569	-8.7760995	\N	\N	12
1324	Ferretería Leogon S.L	physical	42.1459698	-8.8059458	\N	\N	12
1346	Suvema	physical	43.3467796	-8.4160368	\N	\N	12
1347	Sauritech	physical	42.6886419	-2.9219304	\N	\N	12
1348	Reinstalgas	physical	40.4838335	-3.3518054	Avenida de Castilla, 7	\N	12
1349	Hijos de Leto	physical	42.2931597	-5.5182036	\N	\N	12
1350	BricoCentro	physical	38.8535923	0.0028981	\N	\N	12
1351	BricoDénia	physical	38.8377673	0.0906359	\N	\N	12
1370	L'Estaca	physical	42.2654664	2.9614602	\N	\N	12
1371	Ferreteria Realejos	physical	28.3846561	-16.5735174	\N	\N	12
1372	Ferretería Prosperidad_1	physical	37.3819682	-6.0846164	\N	\N	12
1373	Tommy	physical	38.8399941	0.1065955	\N	\N	12
1387	Pachi	physical	41.8288857	-3.0667446	\N	\N	12
1388	Ferretería Hoyo	physical	40.6227206	-3.9063771	\N	\N	12
1389	Bellavista	physical	41.4415896	2.2143407	\N	\N	12
1390	Bauhaus	physical	39.5277622	-0.4396866	\N	https://www.bauhaus.es/es/	12
1391	Iván	physical	38.9615923	-0.1280574	\N	\N	12
1400	Carballido	physical	43.2481491	-8.5829144	\N	\N	12
1401	Cosas	physical	42.4035327	-4.2447925	\N	\N	12
1402	García Teresa	physical	42.4027241	-4.2484216	\N	\N	12
1403	Ferretería V. Miguel	physical	40.5763344	-4.0022327	\N	\N	12
1404	BigMat_2	physical	43.2108532	-8.6917663	\N	\N	12
1405	Ferreteria Maneiro	physical	43.2102547	-8.6920834	\N	\N	12
1406	Pamolux	physical	41.4957691	2.1621745	Carrer de Rizal, 1, Ripollet	\N	12
1407	SEU-B	physical	41.4957566	2.1627042	Carrer de Rizal, 6, Ripollet	\N	12
1408	Ferretería Ripollet	physical	41.4953659	2.1618197	Carrer de Rizal, 1, Ripollet	\N	12
1409	SAE - suministros	physical	43.3846261	-5.7054893	\N	\N	12
1410	Ferretería Ferreparque	physical	28.1400897	-15.4314925	\N	\N	12
1411	Ferretería 29 de Abril	physical	28.1407493	-15.4326411	Calle Veintinueve de Abril, 59, 35007, Las Palmas de Gran Canaria	\N	12
1412	Campo y Hogar_1	physical	36.2825266	-6.0882489	\N	\N	12
1413	Antonio Alonso Medina	physical	28.1386396	-15.4358817	\N	\N	12
1414	Ferretería Guanarteme	physical	28.1374931	-15.4349087	\N	\N	12
1415	La Bodega	physical	36.279545	-6.089317	\N	\N	12
1416	Estructuras y Cubiertas Villarte	physical	28.1359287	-15.4319996	\N	\N	12
1417	Ferretería La Torre	physical	28.1360372	-15.4342841	\N	\N	12
1418	Elté	physical	36.2778333	-6.0872062	\N	\N	12
1419	Almacenes San Pablo	physical	35.8940695	-5.3328985	\N	\N	12
1420	Comercial Muntané Las Palmas	physical	28.1354946	-15.4299897	\N	\N	12
1421	Cin pinturas y barnices	physical	28.131461	-15.4339552	\N	\N	12
1422	Riegotec	physical	28.1315036	-15.4319392	\N	\N	12
1423	Cegrisa	physical	28.1304649	-15.4333531	\N	\N	12
1424	Central de Representaciones Canarias	physical	28.1303741	-15.4344856	\N	\N	12
1425	Ferretería Mas de Gaminde	physical	28.1312201	-15.4339363	\N	\N	12
1426	Grapascan Maquinaria	physical	28.1305866	-15.4312073	\N	\N	12
1427	Velas Linton	physical	28.1304805	-15.4317884	\N	\N	12
1428	Comercial Nolasco	physical	28.1300442	-15.4321108	\N	\N	12
1429	Fedival	physical	36.6778177	-6.1243056	\N	\N	12
1430	Electricidad Mejuto Rodríguez	physical	40.4500082	-3.4684387	\N	\N	12
1431	Ferretería Cañada	physical	28.1178557	-15.4237769	\N	\N	12
1432	Ferretería Sánchez Tarajano	physical	28.1172859	-15.4230794	\N	\N	12
1433	Ferrocasa León y Castillo	physical	28.1177597	-15.4236949	\N	\N	12
1434	Majaelectric	physical	40.4712314	-3.8709019	Calle Gran Vía, 33, 28220, Majadahonda	https://www.majaelectric.com/	12
1435	Ferretería Majariega	physical	40.4715037	-3.8716821	Calle Gran Vía, 32, 28220, Majadahonda	\N	12
1436	Optimus_4	physical	41.4929357	2.1445302	\N	\N	12
1437	Aluminios Almagrán	physical	28.1347027	-15.4362604	\N	\N	12
1438	Came, Carpintería	physical	28.1353039	-15.4356716	\N	\N	12
1439	Cristalería Felipe	physical	28.1361762	-15.4360959	\N	\N	12
1440	Plaza's Ferretería	physical	28.1348285	-15.435969	\N	\N	12
1441	Servicasa	physical	43.2124346	-2.4179425	\N	\N	12
1442	Ferretería Los Llanos	physical	36.7363455	-3.9823423	Carretera de Almería, 80, 29793	http://www.ferreterialosllanos.com	12
1443	Roymar San José	physical	41.6357882	-0.8749589	Camino de Puente Virrey, 74, 50007, Zaragoza	https://www.roymar.es/	12
1444	Ferretería Escrig	physical	39.9913968	-0.0395861	Ronda Magdalena, 49, 12004	https://www.ferreteriaescrig.es/	12
1445	Ferretería Escrig_1	physical	39.9916085	-0.0396927	Calle Ronda Vinatea, 3, 12004	https://www.ferreteriaescrig.es/	12
1449	Ferreteria Santa Ana	physical	37.6518469	-1.01183	Avenida Venecia, 30319, Cartagena	\N	12
1343	Jesús Castro	physical	41.9374143	-4.2449534	\N	\N	12
1344	Bricolaje Rodil	physical	40.4823065	-3.3554499	Paseo de Val, 21, 28804	\N	12
1345	Ferretería Lajares	physical	28.6783464	-13.9375249	\N	\N	12
1352	Puerto	physical	38.7945043	0.1811185	\N	\N	12
1353	Drogas González	physical	41.6432384	-0.8889095	Avenida Francisco de Goya, 24	\N	12
1354	Rodamientos Zaragoza	physical	41.6432715	-0.8917218	Calle de Félix Latassa, 10	\N	12
1355	FECA	physical	41.3496159	1.6896041	\N	\N	12
1356	BricoTecnocasa	physical	39.4631364	-0.3435528	\N	\N	12
1357	Pearte	physical	41.6878961	-0.9751439	\N	\N	12
1358	Repuestos 2010	physical	41.6545374	-0.8997828	\N	\N	12
1359	La Promesa	physical	43.3647415	-8.4238475	\N	\N	12
1360	Ferretería Sánchez Casado	physical	37.6040451	-0.9894352	Calle del Carmen, 35, 30201, Cartagena	\N	12
1361	Ferreteria Feu	physical	41.5464719	2.1041761	Carrer de Colom, 36, 08201, Sabadell	\N	12
1362	Ferretería Josvy	physical	43.6079455	-8.1418519	Avenida Porta do Sol, 22, 15552, Valdoviño	http://bricolink.com	12
1363	Bigmat	physical	41.176442	1.4558179	\N	\N	12
1364	Artehogar	physical	41.6229745	-0.9491377	Avenida Patio de Los Naranjos, 22, 50022	\N	12
1365	Ferretería Ocejo	physical	43.3560034	-3.9572772	\N	\N	12
1366	Ferretaria La Cruz Primera	physical	37.210544	-7.4049081	\N	\N	12
1367	Hermanos Martínez Herrera	physical	42.5168462	-4.0087761	\N	\N	12
1368	Ferretería_10	physical	42.4176324	-4.0428164	\N	\N	12
1369	Ayamar Efectos Navales	physical	37.2135346	-7.4052129	\N	\N	12
1374	Ferretería Méndez	physical	41.3591789	2.0790831	Carrer Urgell, 08940, Cornellà de Llobregat	\N	12
1375	Ferretería Vera	physical	42.7798512	-7.4135034	\N	\N	12
1376	Ferretería Sarria	physical	42.7813507	-7.4156895	\N	\N	12
1377	Martínez e hijos	physical	39.5183735	2.4877629	\N	\N	12
1378	GSI	physical	40.4129438	-3.695506	\N	\N	12
1379	Ferro Logan	physical	38.0795225	-1.2786342	\N	\N	12
1380	Ferretería Santa Clotilde	physical	37.1801627	-3.6128512	Calle Santa Clotilde, 32, 18003, Granada	https://santaclotilde.es/	12
1381	Ferreteria Oroquitq	physical	40.3534742	-3.6914277	Calle del Sáhara, 93, 28041, Madrid	\N	12
1382	Würth_2	physical	40.9898025	-5.6444615	\N	\N	12
1383	Ferretería Ferregar	physical	28.0967547	-15.4145449	\N	\N	12
1384	Cumar Ferretería y Material Eléctrico	physical	28.0964331	-15.4176321	\N	\N	12
1385	Ferretería San José_1	physical	28.0976894	-15.417886	\N	\N	12
1386	Torres Ruiz	physical	36.3666045	-5.2264745	\N	\N	12
1392	Fercasa	physical	36.1361981	-5.4553112	\N	\N	12
1393	Ferretería Enol	physical	40.3882459	-3.7402346	Calle del Pinzón, 38	http://www.ferreteriaindustrialmadrid.com/	12
1394	Ferreteria Vistazul	physical	37.284024	-5.9093435	\N	\N	12
1395	Ferreteria El Llar	physical	43.5372115	-5.6727198	\N	\N	12
1396	Muebles ferretería Julio Sanz	physical	41.8290949	-3.0653346	\N	\N	12
1397	Tenda de Rodrigez	physical	43.1849707	-8.7422904	\N	\N	12
1398	Ferretería La Paz Fuengirola	physical	36.5405132	-4.6340073	C/ San Bernardo, 14, 29640, Las Lauganas-Mijas Costa	https://ferreterialapaz.com/	12
1399	Pedrouzo	physical	43.2119766	-8.6908866	\N	\N	12
1446	Ferretería El Cabo	physical	27.8119207	-17.9148311	\N	\N	12
1447	Aceros y Pinturas	physical	28.1354005	-15.4382174	\N	\N	12
1448	Comercial Muro	physical	28.1343006	-15.4381432	\N	\N	12
1455	Hernández	physical	28.3741551	-16.6535233	\N	\N	12
1456	Grup Lober	physical	41.4967538	2.1618755	\N	\N	12
1457	Effectos Navales SH Duarte	physical	28.9642606	-13.5413189	Calle Agustin de La Hoz Betancort, 10-12	\N	12
1458	Pinturas Valentine	physical	28.9646582	-13.5408494	Calle Agustin de La Hoz Betancort, 20	\N	12
1459	Drogueria Torres	physical	42.5226248	-4.7358015	\N	\N	12
1461	Ferretería Javier	physical	41.4383065	2.2241204	\N	\N	12
1462	Ferreteria Salouan	physical	41.4346167	2.2195407	\N	\N	12
1463	Ferretería Vidal_1	physical	41.4345433	2.2188529	\N	\N	12
1464	Suministros agrícolas El Pino	physical	28.3399609	-16.4150481	\N	\N	12
1465	Ferretería Centro	physical	37.1765224	-3.6040054	\N	\N	12
1466	Bricosur	physical	37.2814277	-5.9212782	Plaza del Emigrante, 6, 41700	https://www.cadena88.com/es/store/bricosur	12
1467	Aluminios Armas	physical	28.1348498	-15.4389649	\N	\N	12
1468	Ferri Weld	physical	42.3524374	-3.6513233	Calle la Bureba, 190, 09007, Burgos	\N	12
1469	Tecnoferr	physical	38.3527098	-2.7399017	Avenida de Andalucía, 77, 23360	http://www.tecnoferr.es	12
1470	Suministros Revuelta	physical	43.3953429	-3.4490391	39750, Colindres	\N	12
1471	Ferretería_11	physical	41.2129396	1.1404647	\N	\N	12
1472	La Cántabra	physical	43.3949537	-3.4520844	Calle de la Magdalena, 39750, Colindres	\N	12
1473	Arcauz	physical	43.2156215	-2.4134155	\N	\N	12
1474	Milagros	physical	40.4687303	-5.7205953	\N	\N	12
1475	Thermomix	physical	40.3910281	-3.6887094	Calle de la Antracita, 7, 28045, Madrid	\N	12
1476	Cipriano Pañeda	physical	43.2756266	-5.6031659	\N	\N	12
1477	Casa Paco	physical	42.7846385	-5.8036689	\N	\N	12
1478	Ferretería Suárez	physical	41.4347376	2.2152969	\N	\N	12
1479	Distribuidora Mogan	physical	27.8864894	-15.7213808	\N	\N	12
1480	Lloifer	physical	41.5668942	2.0242788	\N	\N	12
1481	Aki_1	physical	37.9898503	-0.686998	\N	\N	12
1482	Ferretería Norte	physical	28.1336091	-15.4389406	\N	\N	12
1483	Ganacolor	physical	28.1329059	-15.438667	\N	\N	12
1484	Talleres Palermo	physical	28.1316593	-15.4402117	Calle República Dominicana, 18, 35010	https://tallerespalermo.es	12
1485	Suministros de Fontanería Zec Canarias	physical	28.1325199	-15.4384665	\N	\N	12
1486	Ferretería Argensola	physical	40.4264045	-3.6939825	Calle de Argensola, 30, 28004, Madrid	\N	12
1487	Purificación García del Álamo-Ferretería la Fune	physical	39.4113199	-3.7157324	\N	\N	12
1488	Almacén Cooperativa Frontera	physical	27.7731524	-18.0107377	\N	\N	12
1489	Ferretería Morales	physical	27.7571194	-18.0071511	\N	\N	12
1490	Juno Pinturas	physical	28.2390339	-16.8342966	\N	\N	12
1491	La Ferretería_2	physical	36.0175403	-5.6083757	\N	\N	12
1492	Ferreteria_6	physical	27.7643634	-15.5774746	\N	\N	12
1493	Ferreteria Haria	physical	29.144623	-13.5029537	\N	\N	12
1494	Paco Rodríguez	physical	36.5080537	-6.2749349	Avenida Maconi	\N	12
1495	Inoxnaval	physical	28.9655285	-13.5419664	Calle Hipolito Frias, 12-14	\N	12
1496	Ferreteria La Nueva	physical	36.0153032	-5.6071031	\N	\N	12
1497	Bimca	physical	42.0836433	-8.5063563	\N	\N	12
1498	J. Rivero	physical	41.9434985	-8.8447231	\N	\N	12
1450	Maxivan	physical	37.7189578	-3.9696891	Calle Carrera, 69, 23600, Martos	\N	12
1451	Ferretería Castilleja	physical	37.3861951	-6.0537591	\N	\N	12
1452	Ferretería Ramírez	physical	40.2494456	-3.6970754	Calle de Bélgica, 4, 28320, Pinto	\N	12
1453	La Merced	physical	41.6500806	-4.7198397	\N	\N	12
1454	Suministros Hercal, S.L.	physical	41.5115341	2.1919565	\N	\N	12
1460	Euroconsumo	physical	41.3813748	2.1625278	\N	\N	12
1521	Recanvis Frankjo	physical	41.4917382	2.150836	\N	\N	12
1522	Ferretería Cayetano	physical	38.0426801	-4.0493578	Andújar	\N	12
1523	JSP electrotecnia	physical	40.4327271	-3.641212	\N	\N	12
1524	Almacenes eléctricos Madrileños	physical	40.4335309	-3.633439	\N	\N	12
1536	El Carpin	physical	37.7811517	-5.3890271	\N	\N	12
1537	Materiales de Construcción y Saneamiento Rey	physical	43.4173376	-7.1461623	8-11, 33774, Polígono Industrial El Boutarón	\N	12
1538	Cascanueces	physical	38.385656	-0.416996	\N	\N	12
1539	Ferretería Ortiz	physical	41.6541717	-4.7275043	Calle del General Almirante, 14, 47003, Valladolid	http://www.laferreteria.eu/	12
1553	Multi Lusitano	physical	37.2702056	-7.0227016	\N	\N	12
1554	Hornos de Leña	physical	41.5601635	2.1282851	\N	\N	12
1555	Burgos Ferretería_1	physical	43.3478076	-4.0521167	Calle del Marqués de Santillana, 2, 39300, Torrelavega	\N	12
1556	Ferretería el Escabel	physical	28.4612296	-16.2620562	\N	\N	12
1557	Jama	physical	36.8351462	-2.4587722	\N	\N	12
1558	Mogueme Cerrajeros	physical	28.1066909	-15.4207209	\N	\N	12
1559	Berrazueta	physical	43.3507037	-4.0512782	\N	\N	12
1560	González_1	physical	36.5102959	-6.278003	\N	\N	12
1561	+KLed	physical	43.3747844	-8.4284882	Rúa Manuel Azaña, 23, 15011, A Coruña	\N	12
1562	Ferretería Rincón	physical	43.3486741	-4.0540873	Calle de Lasaga Larreta, 32, 39300, Torrelavega	https://www.ferreteriarincon.es/	12
1563	Ferretería Pacífico	physical	40.4022207	-3.6742543	\N	https://www.ferreteriapacifico.com/	12
1564	JA JS Suministros (Intergas)	physical	40.4443091	-3.4879148	Calle del Invierno, 3	https://martinagenjoinstalaciones.es/	12
1565	Ferrymas_2	physical	41.6508433	-0.8775458	\N	\N	12
1566	Ferretería El Trébol	physical	42.6291662	-0.3216565	Plaza de la Constitución, 3, 22630	http://oscatrebol.com/	12
1567	Ferretería Anglo	physical	43.0075673	-7.5490162	\N	\N	12
1568	Ferretería Gonzalez	physical	43.0111437	-7.5492457	\N	\N	12
1569	Ferreteria Casanova	physical	39.5936263	-0.5875807	\N	\N	12
1570	La Llave_2	physical	38.3834658	-0.7607078	Avenida de la Constitución, 67	\N	12
1571	Bidasoa burdindegia	physical	43.333544	-1.8091822	meatzari kalea, 2	\N	12
1572	Bricofer	physical	41.6674914	-0.8308745	\N	\N	12
1573	Mul-t-lock	physical	41.9806	2.8128161	Carrer de l'Illa, 5	\N	12
1574	El Peso	physical	43.3593516	-5.8483473	Calle Rosal, 56	\N	12
1575	Würth_3	physical	42.5728899	-5.5301622	\N	\N	12
1576	Aluminium Gonper	physical	42.5761682	-5.5323961	\N	\N	12
1577	Servicios de Ferretería VIPE	physical	41.5485493	2.0897802	Carrer de Manuel de Falla, 16, 08206	\N	12
1578	Agrícola del Besaya	physical	43.3472125	-4.0436375	\N	\N	12
1579	Ferretería Torrelavega	physical	43.3482721	-4.0446657	\N	\N	12
1580	Jose Alfonso S.A.	physical	41.6536884	-0.8831478	\N	\N	12
1581	Carpintería Rubimon	physical	39.3988434	-1.6209672	\N	\N	12
1582	Carpe Mare	physical	43.1056913	-9.2175121	Rúa Real, 2, 15124, Muxía	https://www.carpemare.es/	12
1583	Cala Flores	physical	37.6281128	-0.7084761	\N	\N	12
1584	Ferretería La Nueva	physical	43.105218	-9.2176721	\N	\N	12
1585	Recambios Mollet	physical	41.5442616	2.217427	Avinguda d'Antoni Gaudí, 2, 08100, Mollet del Vallès	https://www.recambiosmollet.es	12
1586	Cipernor - Persianas de Seguridad	physical	43.5091792	-5.6819479	\N	\N	12
1587	Sogima	physical	43.5088338	-5.6821875	\N	\N	12
1588	Ferretería Jiménez	physical	37.5244145	-4.9187486	\N	\N	12
1589	Covelo	physical	42.1785651	-8.5360276	\N	\N	12
1590	Siscocan	physical	28.4233114	-16.3183075	\N	\N	12
1591	Suconsa	physical	28.4242155	-16.3181003	\N	\N	12
1592	Ferretería Sánchez_4	physical	28.4272566	-16.3141079	\N	\N	12
1593	Ferretería Panorama	physical	42.4185869	-6.9912019	\N	\N	12
1594	servicio técnico FCR	physical	37.4256456	-5.9845345	Calle Boquerón, 41015, Sevilla	\N	12
1595	Ferretería Solana	physical	38.7242514	-6.5380149	\N	\N	12
1596	Carpena	physical	43.3526447	-4.0487503	\N	\N	12
1597	Ferretería Cantabria	physical	43.3530412	-4.0520467	Avenida de Pablo Garnica, 21, 39300, Torrelavega	https://www.ferrecant.com/	12
1598	CALSI	physical	41.5064608	2.1487071	\N	http://www.calsi.com/	12
1599	Ferretería Iñaki	physical	43.2529387	-2.9384851	\N	\N	12
1600	quîckplâck España	physical	38.0020885	-1.1858905	Autovía del Mediterráneo, 30107	https://www.quickplack.com/	12
1601	Rodaprinsa	physical	43.3557296	-4.046408	\N	\N	12
1602	Juan Cantero	physical	36.7903881	-4.949775	\N	\N	12
1603	Ferretería Jomicom99	physical	40.5766334	-4.0099095	\N	\N	12
1604	Suministros Industriales M. Marcos	physical	42.8464001	-2.6680296	\N	http://www.suministrosmarco.com	12
1605	Almacenes Becerril	physical	43.353561	-4.0455887	\N	\N	12
1606	Castuera	physical	40.5804722	-4.0039635	Calle Escuelas, 14	\N	12
1607	Ferretería Pola	physical	43.2203502	-3.8085436	\N	\N	12
1608	Ferretería Muñoz	physical	40.4628066	-3.6465817	\N	\N	12
1609	Caber	physical	41.9652468	2.8035402	Carrer de Can Pau Birol, 24, Girona	\N	12
1610	Fontanería Crimair	physical	40.622532	-3.9080147	\N	\N	12
1611	El 95	physical	43.3431502	-4.0527738	\N	\N	12
1612	Jurado	physical	39.131654	-4.9337574	\N	\N	12
1613	Rama	physical	39.1324267	-4.9332512	\N	\N	12
1625	Leroy Merlin_18	physical	40.4467768	-3.6981936	Calle de Raimundo Fernández Villaverde, 43, 28003, Madrid	https://www.leroymerlin.es/	12
1626	Ferretería Norte_1	physical	28.6861545	-17.7608588	\N	\N	12
1627	Casa Kishu	physical	28.6830574	-17.76489	\N	\N	12
1628	La Cúpula	physical	28.4104674	-16.5362469	\N	\N	12
1629	BriCor_3	physical	28.4893882	-16.3293459	\N	\N	12
1630	Super Cost	physical	41.6516754	-0.9237085	Calle de Antonio de Leyva, 33, 50011	\N	12
1631	Materiales construcción Pellicer	physical	41.6491261	-0.9211122	Calle de Mosén Jose Bosqued, 6, 50011	\N	12
1632	Comercial Usón	physical	41.63804	-0.8981801	Plaza del Emperador Carlos V, 1	\N	12
1633	Ferretería Sella	physical	43.4640822	-5.0576441	\N	\N	12
1693	Simancas	physical	37.391154	-5.9825581	\N	\N	12
2974	Jomacci	physical	37.3038159	-3.1342008	\N	\N	12
1499	Ferreteria Leirado	physical	42.1311203	-8.4609211	\N	\N	12
1500	Ferreteria Felymar	physical	42.0898304	-8.437729	\N	\N	12
1501	Tecnemel	physical	28.1316453	-15.4390872	\N	\N	12
1502	Maquifer	physical	28.1326997	-15.4402971	\N	\N	12
1503	Ferretería Romero	physical	40.5608248	-4.0148398	\N	\N	12
1504	Cooperativa Virgen de la Salud	physical	39.239071	-0.7735701	\N	\N	12
1505	Ferretería El Árbol	physical	27.9886579	-15.7947854	\N	\N	12
1506	Metalras	physical	41.4673129	2.1916502	camí de les Canyes, 1-2-3, 08924, Santa Coloma de Gramenet	\N	12
1507	Ferreteria Pascual	physical	41.449014	2.2182741	Carrer de Mossen Cinto Verdaguer, 138, 08923, Santa Coloma de Gramenet	\N	12
1508	La Lampisteria By Climalectric	physical	41.4533844	2.2080909	Carrer Major, 17, 08921, Santa Coloma de Gramenet	https://www.climalectric.com	12
1509	Lozano Materials per a la construcció	physical	41.4427146	2.2107785	Avinguda de la Generalitat, 129, 08923, Santa Coloma de Gramenet	\N	12
1510	Febricat	physical	41.4584177	2.2022643	Carrer d'Enric Granados, 32, 08924, Santa Coloma de Gramenet	\N	12
1511	Ferreteria Medina	physical	41.4549208	2.2064472	Carrer del Doctor Ferran, 21, 08921, Santa Coloma de Gramenet	\N	12
1512	Vial Public	physical	41.4696336	2.1911103	Carretera de la Roca, 08924, Santa Coloma de Gramenet	\N	12
1513	Ferretería Domínguez Hijos	physical	28.1304657	-15.4414764	\N	\N	12
1514	Ferretería Afroa	physical	28.1308994	-15.4421361	\N	\N	12
1515	Precaución Seguridad Laboral	physical	28.1309911	-15.4436629	\N	\N	12
1516	Maquinaria Macservi	physical	28.1272378	-15.4427059	\N	\N	12
1517	Ferrecons de la Plata	physical	38.5641821	-6.3345534	\N	\N	12
1518	V. Marí	physical	38.9847378	1.535176	\N	\N	12
1519	Mega Smile	physical	42.2135075	-8.7552158	\N	\N	12
1520	Ferretería Lute	physical	39.9067262	-1.3663495	\N	\N	12
1525	Toldos Vilassar	physical	41.5079967	2.3881915	\N	\N	12
1526	CGR Rètols	physical	41.508945	2.375124	\N	\N	12
1527	Ferretería Rubeltor	physical	36.7780647	-4.1047997	\N	\N	12
1528	Ferretería Ceto	physical	43.1545754	-4.6266696	Calle de Eduardo García de Enterría, 28, 39570	\N	12
1529	Biniflex	physical	41.6341708	2.2987229	\N	\N	12
1530	Cerrallería Conxo	physical	42.8696811	-8.5534375	Rúa do Doutor Maceira, 21, 15706, Santiago de Compostela	\N	12
1531	Construdeco	physical	43.6357085	-7.6021628	\N	\N	12
1532	Ferretería Nautica	physical	43.4482359	-3.7689181	\N	\N	12
1533	Ferretería Circunvalación	physical	37.2203664	-3.6842649	Calle Maracena, 18230, Atarfe	\N	12
1534	Ferretería Sánchez_3	physical	37.2225194	-3.691065	Avenida de la Estación, 19, 18230, Atarfe	https://www.tuferreteronline.com	12
1535	Pulido	physical	40.4254887	-3.5551352	\N	\N	12
1540	Ferretería Alisios	physical	28.428036	-16.3072515	\N	\N	12
1541	Ferreteria Orfila	physical	39.8503679	4.2580977	Carrer de Sant Lluís, 37, 07711	\N	12
1542	Ferretería Santana	physical	28.008094	-15.5386696	\N	\N	12
1543	Corona	physical	42.1652897	0.8944747	Rambla del Doctor Pearson, 13, 25620, Tremp	\N	12
1544	Suministros Industriales Juan González Parra	physical	37.2155866	-1.8907053	\N	\N	12
1545	Aguilar	physical	41.1658758	-2.4216941	\N	\N	12
1546	Ferreteria Cerezo	physical	40.3514726	-3.729043	\N	\N	12
1547	El Hórreo_2	physical	42.867735	-8.5541045	García Prieto	\N	12
1548	Ferretería Avenida_2	physical	38.6004946	-0.0488306	\N	\N	12
1549	Ferretería Ripoll	physical	38.6014963	-0.0478549	\N	\N	12
1550	Burgos Ferretería	physical	43.347791	-4.0520975	\N	\N	12
1551	Maquinaria Agrícola Palencia - González	physical	43.3428137	-4.0514907	\N	\N	12
1552	Brico Center	physical	41.4992144	2.1604586	\N	\N	12
1614	Ferretería Bike Luna	physical	38.3566826	-2.8023821	\N	\N	12
1615	Ferretería Luna_1	physical	38.3542826	-2.8032813	\N	\N	12
1616	Accesorios Louro	physical	42.1610839	-8.6286267	\N	\N	12
1617	Brico Vega	physical	43.3460645	-4.0571367	Avenida del Besaya, 3, 39300, Torrelavega	\N	12
1618	Ferretería-Drogería "Mario"	physical	37.1368649	-3.6671528	\N	\N	12
1619	Ferretería_12	physical	40.2931102	-3.8224501	\N	\N	12
1620	Accessorios Louro	physical	42.0663329	-8.6292279	\N	\N	12
1621	Ferreteria Mino	physical	42.1039706	-8.5561929	\N	\N	12
1622	Ferreteria Barral_1	physical	42.1038202	-8.5609735	\N	\N	12
1623	R. Fernandez	physical	42.0683417	-8.5890466	\N	\N	12
1624	Ferretería Gomar	physical	43.3447417	-4.0614071	Plaza de Covadonga, 4, 39300, Torrelavega	\N	12
1634	Panizo	physical	43.295581	-2.9885177	\N	\N	12
1635	Monnelleta España	physical	41.6424141	-0.8735096	Calle del Escultor Félix Burriel, 6	\N	12
1636	Comercial Quemoil	physical	41.6443739	-0.8757909	Calle Manuel Lorenzo Pardo, 30, 50008	\N	12
1637	Aclos	physical	41.6437335	-0.8710849	Calle del Monasterio de Poblet, 6	\N	12
1638	Cristalería Europa	physical	41.641226	-0.8694085	Calle Privilegio de la Unión, 58	\N	12
1639	Droguería Tello	physical	41.6423653	-0.8682352	Calle Miguel Servet, 73	\N	12
1640	Hipopótamo	physical	41.6412063	-0.8731644	Calle Antonio Maura, 4	\N	12
1641	Ferrokey_1	physical	38.3975005	-0.4366254	\N	\N	12
1642	An de Juan	physical	40.6217841	-4.024814	Calle Vicente Guillén Zamorano, 22	http://www.ajcenter.es/	12
1643	Electricidad Adrián Martín	physical	40.5799412	-4.002253	Calle de San Gregorio, 36	\N	12
1644	Penwater Piscinas y Spa	physical	40.5768768	-4.0048509	Plaza del Caño, 1	http://piscinas-penwater.com/	12
1645	Tien21 JM Rodilla	physical	40.5577645	-5.6731717	\N	\N	12
1646	Ferretería Larrea	physical	42.4664262	-2.4430127	\N	\N	12
1647	Camino a casa	physical	40.446898	-3.523016	\N	\N	12
1648	Iberdrola	physical	40.4598942	-3.6856349	\N	\N	12
1649	BriCor_4	physical	40.4297058	-3.7168497	\N	\N	12
1650	Ferrecasa	physical	40.4793113	-3.6707401	\N	\N	12
1662	Ferretería Galaica	physical	42.7795574	-7.4109686	\N	\N	12
1663	Ferretería Kayma	physical	28.1055985	-15.4150539	\N	\N	12
1665	Ferretería Sánchez_5	physical	37.2260107	-3.6851555	Calle Cedazos, 61, 18230, Atarfe	http://ferreteria-sanchez.es/es	12
1666	Bricordino_1	physical	28.1487707	-15.4285147	\N	\N	12
1667	Bricordino Ferretería	physical	28.1487029	-15.4287892	\N	\N	12
1668	Can Mateu	physical	39.7146927	2.9104743	\N	\N	12
1669	Ferretería Sindo	physical	42.8591686	-8.6536407	Avenida da Maía, 47, 15220, Bertamiráns	\N	12
1670	Debarán	physical	41.0679683	-2.6438716	\N	\N	12
1671	Bigmat Fontecha	physical	42.351082	-3.6487409	Calle Alcalde Martín Cobos, 15, 09007, Burgos	https://fontecha.bigmat.es/site	12
1651	Ferretería Puerta de Madrid	physical	40.1709178	-3.8120971	Avenida Europa, 4, 28977, Casarrubuelos	http://www.ferreteriapuertademadrid.com/	12
1652	Mármoles Hermanos Álvarez Sampedro	physical	43.4222803	-4.7612033	\N	\N	12
1653	Ferretería Merino	physical	39.9658829	-4.8157418	\N	\N	12
1654	Ferreteria Industrial Besós	physical	41.4471512	2.1998193	\N	\N	12
1655	Humberto	physical	43.3910286	-5.6637961	\N	\N	12
1656	Optimus_5	physical	41.7241378	2.9268577	\N	\N	12
1657	BricoXavia	physical	38.7815388	0.1799187	\N	\N	12
1658	VOLTA, S.L.	physical	41.4946888	2.1530127	\N	\N	12
1659	Keerl	physical	41.3985762	2.1501122	Carrer de Marià Cubí, 42	\N	12
1660	Brikopex Ferretería	physical	43.4618302	-5.0585727	\N	\N	12
1661	Ferreteria Marina	physical	41.3517903	2.1079675	Rambla de la Marina, 301, L'Hospitalet de Llobregat	\N	12
1664	Gárate	physical	42.022384	-3.2865391	\N	\N	12
1672	Covecano	physical	27.8055974	-17.9148327	Calle San Francisco, 12, 38900	\N	12
1673	Guarrería Daniel Gil de Avalle	physical	37.1734515	-3.5942297	Plaza del Realejo	\N	12
1674	Cano	physical	40.1262427	-5.6590697	\N	\N	12
1675	La Janina Hermanos	physical	40.4562973	-3.4787345	\N	https://ferreteria-la-janina-hermanos.negocio.site/	12
1676	Ferreteria Logan-Saló	physical	41.9679326	2.8234038	\N	\N	12
1677	Comafe	physical	40.4357077	-3.6993068	\N	\N	12
1678	El Teide	physical	28.4380145	-16.3052076	\N	\N	12
1679	Ferretería Leonesa	physical	40.432781	-3.6856975	\N	\N	12
1680	jcobos	physical	40.4448001	-3.6989292	\N	\N	12
1681	Ferretería Casanova	physical	41.6507675	-0.8759129	\N	\N	12
1682	Toycasa	physical	28.4437766	-16.312171	\N	\N	12
1683	INAUPI Suministros Industriales	physical	39.9713874	-0.0769217	\N	https://www.inaupi.com/	12
1684	SIR Suministros Industriales y Recambios	physical	39.9715971	-0.0562379	\N	https://sir.es/	12
1685	LIMAC Materiales de Construcción	physical	39.9646325	-0.0649135	\N	http://www.limac-castellon.com/	12
1686	Comercial IBA	physical	39.9713812	-0.0556847	\N	https://www.comercialiba.com/	12
1687	Cofac	physical	41.6140322	2.0885705	\N	\N	12
1688	Ferretería Ferreiro	physical	42.8593079	-8.6531355	\N	\N	12
1689	Ferretería Manuel	physical	43.6610998	-8.0561882	\N	\N	12
1690	Ferretería O Triqui	physical	43.6605918	-8.0539971	\N	\N	12
1691	Sa Rota	physical	38.9988248	1.5452898	\N	\N	12
1692	Haomai Hipermarket	physical	42.8601198	-8.6489573	\N	\N	12
1698	Pradiño Comercial	physical	42.7634536	-8.0167644	\N	\N	12
1699	Ferretería Hernández	physical	40.578624	-4.0040379	\N	\N	12
1700	Ferro-bric	physical	40.4364621	-3.8159813	\N	\N	12
1701	Ferreteria Marin	physical	36.8536139	-2.3555507	\N	\N	12
1702	Ferretería Gómez Hermanos	physical	40.4859048	-3.3551547	Calle Miguel de Moncada, 4, 28805	\N	12
1703	Hidráulica Basilio S.L.	physical	28.1559952	-15.418935	\N	\N	12
1704	Ferretería Sampere	physical	41.6148624	2.0883388	\N	\N	12
1705	Piscines Catellar	physical	41.6132704	2.0831194	\N	\N	12
1706	Pampín Martínez S.L.	physical	42.7943563	-8.1690087	Rúa de Manuel Iglesias, 35, 36590, Vila de Cruces	\N	12
1707	Sol	physical	40.0302454	-6.087783	\N	\N	12
1708	Grúas y Elevadores	physical	28.1653638	-15.4050316	\N	\N	12
1709	Albatros, Suministros Industriales	physical	28.1591975	-15.4137566	\N	\N	12
1710	Grupo Disco Canarias, Suministros Industriales	physical	28.1614601	-15.4116912	\N	\N	12
1711	Medifonsa, Hierros y Aceros	physical	28.1586184	-15.4136163	\N	\N	12
1712	Contenur, Contenedores	physical	28.1620096	-15.410151	\N	\N	12
1713	Puerto Market, Suministros Industriales	physical	28.16215	-15.4100022	\N	\N	12
1714	Hierros 7 Islas	physical	28.1630123	-15.4091425	\N	\N	12
1715	Cabos y Redes	physical	28.1628624	-15.4088166	\N	\N	12
1716	Lifechems	physical	28.1597243	-15.4112279	\N	\N	12
1717	Servecan	physical	28.1599629	-15.4117762	\N	\N	12
1718	Anidia	physical	28.1583823	-15.413369	\N	\N	12
1719	King Hogar	physical	28.1585415	-15.4132142	\N	\N	12
1720	Wrist Ship	physical	28.157647	-15.4141213	\N	\N	12
1721	Eyser Hidráulica, Servicios Hidráulicos y Neumática	physical	28.1546604	-15.4207465	\N	\N	12
1722	Comercial Rofer, Suministros navales	physical	28.1549599	-15.4206882	\N	\N	12
1723	Rodamientos Gallardo	physical	28.1549124	-15.4192765	\N	\N	12
1724	Alfa 90	physical	28.1543714	-15.4172546	\N	\N	12
1725	Ber Hostel, Maquinaria de Hostelería	physical	28.1535104	-15.418526	\N	\N	12
1726	El Extinguidor	physical	28.1531123	-15.4179434	\N	\N	12
1727	Montajes Berpal	physical	28.1560152	-15.4193687	\N	\N	12
1728	Hidráulica Gopar	physical	28.1560434	-15.4201804	\N	\N	12
1729	Germán Hernández Melián	physical	28.1562632	-15.4178682	\N	\N	12
1730	Almacenes Grau-Bassas	physical	28.156266	-15.4179687	\N	\N	12
1731	Morpul	physical	28.1568984	-15.4184964	\N	\N	12
1732	Sánchez Arencibia	physical	28.1568799	-15.4182413	\N	\N	12
1733	Hidrokalor Canarias	physical	28.1568626	-15.417485	\N	\N	12
1734	Inprecasa	physical	28.1568499	-15.4169748	\N	\N	12
1735	Anidia_1	physical	28.1579786	-15.4209285	\N	\N	12
1736	IASO	physical	28.1577823	-15.4202211	\N	\N	12
1737	Oms y Viñas, Suministros de hostelería	physical	28.1577015	-15.4179546	\N	\N	12
1738	Ramón	physical	43.0298366	-7.3275505	\N	\N	12
1739	La Estación_1	physical	40.033105	-6.0801056	\N	\N	12
1740	Pereira	physical	42.4165822	-6.9871857	\N	\N	12
1741	Maquinaria Tony y Javi	physical	43.0299767	-7.3259592	\N	\N	12
1742	Canaima	physical	43.4933563	-8.2128742	Estrada do Mestre García Niebla, 12, 15404, Ferrol	https://tienda.canaima.es/pagina/catalogo	12
1743	La Botigueta	physical	41.6133232	2.086131	\N	\N	12
1744	Can Pins	physical	39.7698941	3.0235097	carrer Església, 07420	\N	12
1745	Casa Subiza	physical	42.6719142	-1.815354	\N	\N	12
1801	Ferretería Encarna_1	physical	37.6107811	-2.9319037	Calle Puerta Real, 27, 18813, Cuevas del Campo	\N	12
1802	Bricolaje Arturo	physical	38.089316	-0.7128183	Avenida de Justo Quesada, 41	\N	12
1803	Ferretería Alayon	physical	28.0520809	-16.7178268	Calle Juan XXIII, 6	\N	12
1804	Ferreteria_7	physical	28.0528926	-16.709889	\N	\N	12
1805	G3	physical	42.360819	-3.6791294	\N	\N	12
1806	Comercial Álvaro Blanco	physical	42.42055	-6.9798154	\N	\N	12
1819	Cadena 88_2	physical	37.2109478	-3.6218337	Calle de Luis Buñuel, 6, 18197, Pulianas	https://www.cadena88.com	12
1820	Icar	physical	41.3669464	-6.1046111	\N	\N	12
1821	Rodríguez	physical	43.2989037	-2.9925462	\N	\N	12
1822	Panizo_1	physical	43.295072	-2.9862907	\N	\N	12
1694	La Ferretería de Carlos	physical	43.3351317	-4.0446552	\N	\N	12
1695	M. Sáez Ferretería	physical	41.4450549	2.2186705	\N	\N	12
1696	Subministres Salouan	physical	41.4433692	2.2241347	\N	\N	12
1697	Ferretería Balboa	physical	42.7632297	-8.020805	\N	\N	12
1746	Denetarik	physical	43.4174536	-2.7269035	\N	\N	12
1747	Iturriaga	physical	43.4175892	-2.7274168	\N	\N	12
1748	Beracal SL.	physical	43.1566755	-8.5660147	Rúa Xaquín Lorenzo, A Silva, 15186, Cerceda	\N	12
1749	Agirre	physical	43.4206173	-2.7257732	\N	\N	12
1750	Ferretería del Barrio	physical	40.4385395	-3.7081749	Calle de Vallehermoso, 90	\N	12
1751	La Plataforma de la Construcción_1	physical	40.4047072	-3.6984734	\N	\N	12
1752	Comercial Galán	physical	39.872424	-3.9488297	\N	\N	12
1753	Instalaciones Jesús	physical	39.8038056	-4.0232189	\N	\N	12
1754	Ferretería Logroño	physical	42.4645218	-2.4359387	Avenida de La Paz, 56	\N	12
1755	Ferretería Casado	physical	42.462623	-2.4543643	Avenida Pérez Galdós, 59	\N	12
1756	Ferretería Pérez	physical	38.8590262	-6.1030615	\N	\N	12
1757	Centro	physical	38.9091331	-6.6161681	Calle Felipe Checa, 06480, Montijo	\N	12
1758	Ferretería Las Palomas	physical	37.2473982	-1.7976131	\N	\N	12
1759	La Chispa_1	physical	41.4093775	2.1887425	\N	\N	12
1760	Gerbusa SL	physical	42.5523267	-3.3220621	\N	\N	12
1761	Julio Reviejo	physical	39.9630887	-4.8196286	Calle Cervantes, 45600, Talavera de la Reina	\N	12
1762	Ferretería Rinconada	physical	40.4769735	-3.3691129	\N	\N	12
1763	Ferreteria Santos	physical	41.3736455	2.1056276	\N	\N	12
1764	Raparàpid	physical	41.9322874	2.25253	\N	\N	12
1765	Lledó Ferreters	physical	41.5265086	2.2274039	avinguda de Badalona, 30, 08105, Sant Fost de Campsentelles	\N	12
1766	O'Keys Center	physical	39.9692707	-4.8254168	Avenida de Juan Carlos I, 64, 45600, Talavera de la Reina	\N	12
1767	Ferretería Dacio Armas González	physical	27.7607136	-18.0085067	Carretera Las Lajas, 38, 38911	\N	12
1768	Ferretería Congosto	physical	40.3728901	-3.6191469	\N	\N	12
1769	Marco multitienda	physical	42.275157	-0.6867619	\N	\N	12
1770	El Barbero e Hijas, S.L	physical	37.0074792	-3.0107528	\N	\N	12
1771	Alcer	physical	41.385743	2.1379585	Carrer de Nicaragua, 103, 08029, Barcelona	\N	12
1772	Lombardero	physical	43.1595747	-7.6927997	\N	\N	12
1773	Hermanos Pena	physical	43.5006282	-8.2030581	Rúa Cristóbal Colón, 41-43	\N	12
1774	Ferreteria Font	physical	41.9309798	2.2531602	\N	\N	12
1775	Alba	physical	41.9316378	2.2532192	\N	\N	12
1776	Selmacon	physical	42.3501745	-3.6587817	Naves Azucarera, D3, 09007, Burgos	https://www.selmacon.com/	12
1777	Imar	physical	40.6561332	-6.104296	\N	\N	12
1778	Ferretería Venecia_1	physical	40.4465209	-3.710967	\N	\N	12
1779	J y J	physical	40.5674716	-3.5067555	\N	\N	12
1780	Partida	physical	40.7137126	-4.0729498	\N	\N	12
1781	Ferreteria Rodriguez	physical	40.4979851	-4.0655128	\N	\N	12
1782	Ferretería Santa Clotilde_1	physical	37.2230572	-3.6408973	Calle Alquife, 18220, Albolote	https://santaclotilde.es/	12
1783	FULL	physical	42.3599329	-3.6472523	\N	\N	12
1784	El Pozu	physical	43.16839	-5.741319	\N	\N	12
1785	Joanfer	physical	40.4772277	-3.7134533	\N	\N	12
1786	Brico Canyada Ferretería	physical	39.5274536	-0.4886972	\N	\N	12
1787	Arte Bric	physical	42.4173494	-6.9884243	\N	\N	12
1788	H. Nogal Bravo S.L.	physical	40.4997172	-4.0642791	\N	\N	12
1789	Ferretería Moncho	physical	42.4159725	-6.9816115	\N	\N	12
1790	Ferretería Venecia_2	physical	40.4396955	-3.7126581	\N	\N	12
1791	Ferretería El Cardón	physical	28.3723318	-16.8529132	\N	\N	12
1792	d.Luz	physical	43.2173289	-8.1885082	\N	\N	12
1793	Ferrokey_2	physical	40.3558628	-3.9021379	Avenida del Príncipe de Asturias, 127, 28670, Villaviciosa de Odón	\N	12
1794	Ferretería González	physical	28.6603561	-17.9164364	\N	\N	12
1795	Ferreteria Bruc	physical	41.3962895	2.1666968	Bruc, 115	\N	12
1796	La Valla - Cadena 88	physical	40.4069454	-3.8792388	\N	\N	12
1797	Ferreteria Dalmau	physical	42.0038015	2.2844409	Passeig de Sant Joan, 144, 08560, Manlleu	\N	12
1798	Ferretería Ferroarzola	physical	28.0307003	-17.1982006	\N	\N	12
1799	Ferretería Buelna	physical	43.2610577	-4.0696126	Calle Trabajadores de Authi, 1, 39400, Los Corrales de Buelna	\N	12
1800	El Almacén	physical	43.1678701	-5.7372439	\N	\N	12
1807	Rayglo	physical	37.8833453	-4.7731558	\N	\N	12
1808	Talleres Peña y Jurado	physical	38.0474526	-4.1716456	23770, Marmolejo	\N	12
1809	Ferretería Rafael	physical	38.0861851	-0.7447921	\N	\N	12
1810	Ferretería Rafal	physical	38.1032808	-0.8509463	\N	\N	12
1811	Ferretería Papelería Adiario	physical	41.4668971	-1.0843296	\N	\N	12
1812	Ferretería Lugo	physical	43.0104866	-7.5546748	\N	\N	12
1813	Comercial Eléctrica	physical	28.6534828	-17.9115619	Calle Pedro Miguel Hernández Camacho, 22	\N	12
1814	Barrutxi	physical	42.9953974	-3.0109684	\N	\N	12
1815	D. Hernández e Hijos	physical	43.383728	-3.2205942	\N	\N	12
1816	Sainz	physical	41.6519267	-4.7239002	\N	\N	12
1817	Trillo	physical	39.5128896	2.5368832	\N	\N	12
1818	Ferretería José Suárez López	physical	27.8385773	-15.4488694	\N	\N	12
1823	El Cinturón	physical	41.3676707	2.1340034	Rambla de Badal, 46, 08014, Barcelona	https://elcinturon.es	12
1842	La Llave_3	physical	42.0045113	-4.5239362	\N	\N	12
1843	Bauhaus_1	physical	41.9660933	2.7807874	\N	\N	12
1851	H2 Moda y Hogar	physical	39.2025539	-0.5064522	Avinguda de Carlet, 68, 46250, L'Alcúdia	\N	12
1852	Ferreteria el Mercat	physical	39.194022	-0.5059431	Carrer Verge de l'Oreto, 5, 46250, L'Alcúdia	\N	12
1853	Ferretería Perello	physical	37.9788393	-0.6812887	\N	\N	12
1854	Quim	physical	41.8608424	2.664471	\N	\N	12
1855	PH y CLORO	physical	39.1928371	-0.5065325	Carrer de Blasco Ibáñez, 16, 46250, L'Alcúdia	\N	12
1856	Isabdaretillo	physical	41.5267896	2.1140717	Carrer d'Elcano, 79, 08204	\N	12
1857	Bande	physical	42.033305	-7.974693	\N	\N	12
1858	CMB Bricolage	physical	40.3972776	-3.6177902	Bulevar de José Prat, 41, 28032, Madrid	\N	12
1859	Brico Express	physical	41.612958	2.3057177	\N	\N	12
1860	Ferretería Virgen de Luján	physical	37.3744127	-6.0019192	\N	\N	12
1861	Ferretería Rodriguez	physical	42.8672352	-5.3220932	Calle Ángel Ruiz, 12, 24850, Boñar	\N	12
1862	Sucesores de Moreno	physical	40.9727943	-5.6657133	\N	https://www.sucesoresdemoreno.com	12
1863	Fernandez Solis	physical	43.5628443	-5.9743758	\N	\N	12
1864	Ferretería Fontanería Ros	physical	37.9770359	-0.6853108	\N	\N	12
1824	Ferreteria Adam	physical	41.3803908	2.1703679	Hospital, 73	\N	12
1825	Lorenzo	physical	42.1016997	-8.5578911	\N	\N	12
1826	Ferrcash	physical	40.3461761	-3.5219932	\N	\N	12
1827	Subministraments Vimor	physical	41.4328399	2.2188143	\N	\N	12
1828	Ferretería Pontevedra	physical	42.4285121	-8.6303614	\N	\N	12
1829	Dilmar	physical	41.4000935	2.1706083	Carrer de Roger de Flor, 185	\N	12
1830	Seguritek	physical	41.3942154	2.172346	Carrer de la Diputació, 312	\N	12
1831	Mon Clau	physical	41.3893038	2.1544871	\N	\N	12
1832	Santi	physical	43.3036261	-2.9735805	Calle Obieta	\N	12
1833	Ferretería Vilamar	physical	38.5093211	-0.2299018	\N	\N	12
1834	Ferretería Méndez_1	physical	36.9994884	-1.8950881	\N	\N	12
1835	Superlux	physical	41.3669463	2.1344463	08014, Barcelona	https://www.pulidoresbarcelona.com/	12
1836	Guria	physical	43.2190064	-2.8182953	\N	\N	12
1837	Eduardo Herrero	physical	40.3564633	-5.5257658	\N	\N	12
1838	Brico idea	physical	36.6114269	-4.5163971	Calle Antonio Alcaide Sanchez, 23, 29620	\N	12
1839	Navaluenga	physical	40.4127854	-4.7088423	\N	\N	12
1840	Ferreteria Antoner	physical	41.8640308	2.6635735	Carrer d'Anselm Clavé, 1, Santa Coloma de Farners	\N	12
1841	Bazar y Ferretería Zamorita	physical	37.9401425	-3.7279344	\N	\N	12
1844	Eleuterio Básculas	physical	37.1317529	-3.6747125	Calle Real de Málaga, 70	http://basculas-eleuterio.es	12
1845	El arca de noé	physical	37.3775538	-6.0500936	\N	\N	12
1846	Hostelux	physical	39.160713	-0.2627948	\N	\N	12
1847	Bricolaje Zacarias	physical	42.0003732	-4.5100818	\N	\N	12
1848	La Llave_4	physical	43.3705837	-8.4029183	\N	\N	12
1849	Rigau_2	physical	41.9618659	2.8043046	Carretera de Santa Coloma, 82	\N	12
1850	El Duplicador	physical	41.9952821	2.820485	\N	\N	12
1925	FERDONOR, SL	physical	42.9735037	-8.4409326	6, 15688	\N	12
1926	Serralleria Jate	physical	41.6739896	2.3975765	\N	\N	12
1927	Machaco	physical	40.2789791	-4.3066017	\N	\N	12
1928	Casa Calvo	physical	43.0794751	-8.4060782	Rúa Alfonso Senra, 49, 15680, Ordes	\N	12
1929	Ferreteria Vives	physical	41.7930444	0.8103969	Carrer d'Urgell, 18, 25600, Balaguer	\N	12
1930	Ferretería Biedma	physical	38.0148959	-3.3708954	Avenida de la Libertad, 23400, Úbeda	\N	12
1931	Casa Florida	physical	40.4231644	-3.7238017	\N	\N	12
1932	La Llave_5	physical	43.2514395	-2.947781	Camilo Villabaso kalea / Calle Camilo Villabaso	\N	12
1969	Ferreteria El Pasaje	physical	39.433701	-0.471842	Carrer de Sant Fermí, 12, 46900, Torrent	\N	12
1970	El Clau Torrent	physical	39.4359008	-0.4670271	Avinguda Al Vedat, 24, 46900, Torrent	\N	12
1971	El Clau Torrent_1	physical	39.4274129	-0.4770742	Carrer del Pare Méndez, 168, 46900, Torrent	\N	12
1972	Ferreteria Sufespa	physical	39.4378546	-0.4696467	Carrer Músic Mariano Puig Yagov, 6, 46900, Torrent	\N	12
1973	Kcenter	physical	39.433743	-0.469375	Carrer d'Albocàsser, 2, 46900, Torrent	\N	12
1974	Ferreteria San Valeriano	physical	39.433369	-0.476693	Carrer de Sant Valerià, 26, 46900, Torrent	\N	12
1975	Ferreteria Jove	physical	39.4343219	-0.479055	Carrer del Camí Reial, 102, 46900, Torrent	\N	12
1976	Taller Hierro Aluminio	physical	39.439884	-0.468861	Carrer de València, 87, 46900, Torrent	\N	12
1977	Ferreteria La Llave	physical	39.4369455	-0.4650775	Carrer de Sagra, 1, 46900, Torrent	\N	12
1978	Ferreteria Hnos. Rodrigo	physical	39.430843	-0.474815	Avinguda Al Vedat, 108, 46900, Torrent	\N	12
1979	Ferreteria El Trebol	physical	39.433544	-0.470055	Avinguda Al Vedat, 83, 46900, Torrent	\N	12
1980	Ferreteria I Electricitat Parc Central	physical	39.423981	-0.468483	Carrer d'Atenes-04, 19, 46900, Torrent	\N	12
1981	La Clau d'alba Cerrajeros	physical	39.437237	-0.47052	Carrer de Sant Enric, 13, 46900, Torrent	\N	12
1982	BricoCentro_1	physical	42.0069853	-4.520064	\N	\N	12
1983	Sani 2000	physical	42.0064626	-4.5201879	\N	\N	12
1984	Ferreteria Herradura	physical	37.3411503	-6.0589797	Avenida de la Filosofía, 22, 41927, Mairena del Aljarafe	\N	12
1985	Pitarque Robots	physical	40.4460424	-3.6705978	\N	\N	12
1986	Ferretería Desiré	physical	36.7227351	-4.5383199	Calle Van Gogh, 13, 29590	\N	12
1987	Mabe	physical	39.4833955	-6.3656378	Calle Sorolla	\N	12
1988	Edyma	physical	39.5610044	3.3713158	\N	\N	12
2003	Ferreteria Candau_1	physical	41.5390289	2.4332054	Ronda de Leopold O'Donell, 55, 08302, Mataró	https://www.ferreteriacandau.com/	12
2005	Ferretería Veiga, S.L.	physical	43.015605	-7.5656104	Rúa Ourense, 78, 27004, Lugo	https://www.ferreteriaveiga.com/	12
2006	Ferretería Europa	physical	43.4100739	-3.4126082	Plaza de Cachupín	\N	12
2007	Ferreteria Feycofe	physical	43.4115873	-6.1584337	Cornellana	\N	12
2008	Arguia	physical	43.2094051	-2.8866456	Calle Severo Ochoa	\N	12
2009	Ferretería Rucho	physical	42.8089209	-7.1085066	\N	\N	12
2010	Riagal	physical	43.490765	-8.2199279	Rúa Pintor Bello Piñeiro, 19, 15404	https://www.riagal.com/	12
2011	Ferretería Cabrales	physical	43.3028294	-4.8161327	Calle Basilio de Mestas, Arenas de Cabrales	http://www.ferreteriacabrales.com	12
2012	Mercurio	physical	43.538963	-5.6561006	Calle Uría, 17	\N	12
2013	Bricopinares	physical	42.0216575	-3.284242	\N	\N	12
2014	La Herramienta Balear	physical	39.5296591	2.5102637	\N	\N	12
2015	Electricidad Serapio Calvo	physical	40.5792926	-3.9553015	\N	\N	12
2016	FSáenz	physical	36.7448039	-4.421853	Calle Emilio Thuillier, 54, 29014	http://fsaenz.com	12
2017	Galmés	physical	39.7038745	3.1049289	\N	\N	12
2018	Ferretería Hnos Cotera Ibañez	physical	43.3155457	-4.8475747	Carreña	\N	12
2019	Bricogaudí-Optimus	physical	42.458653	-6.0554929	Avenida de las Murallas, 46	\N	12
2036	Sifix	physical	39.6087894	2.6728232	\N	\N	12
2037	Ferretera Española	physical	43.463051	-3.8092278	Calle del Cubo, 1, 39001, Santander	http://www.ferreteraespanola.es	12
2038	Ferrmoral	physical	40.6795105	-3.9730498	\N	\N	12
2039	González_2	physical	43.3604428	-8.4098928	\N	http://www.gonzalezferreteria.com/	12
2040	Würth_4	physical	39.6109291	2.6643567	\N	\N	12
2041	Hilti_1	physical	39.609224	2.6616844	\N	\N	12
2042	Ferretería Ferrovilla	physical	40.3597559	-3.9092955	Calle de Fernando III, 28670, Villaviciosa de Odón	\N	12
2043	Ferreteria Tombas	physical	41.2611573	1.1710114	Carrer de l'Onze de Setembre, 43460, Alcover	\N	12
2044	Ferreteries Ustrell	physical	41.3597816	2.1007043	\N	\N	12
2045	Ferretería el gato	physical	37.9088566	-4.7799048	Calle Juan Latino, 12	https://ferreteriaelgato.negocio.site/	12
2046	Jeymo Jardín	physical	40.5621569	-4.0141263	\N	\N	12
1865	Ferretería Virgen del Valle	physical	37.3751995	-5.9980976	\N	\N	12
1866	ISE40	physical	41.4473333	2.20808	Carrer de la Cultura, 40, 08922	\N	12
1867	Luga	physical	42.8312375	-1.6080339	\N	\N	12
1868	Manolín	physical	37.4748454	-4.4403065	Avenida Pedro Iglesias, Cabra	\N	12
1869	Ferretería Echevarría	physical	37.3766689	-5.9977879	\N	\N	12
1870	Telas metálicas	physical	42.8567635	-2.663584	\N	\N	12
1871	Comercial Ovetense	physical	43.3571977	-5.8489551	Calle González Besada, 6, 33007, Oviedo / Uviéu	https://www.roalba.com/indexquienes.php	12
1872	Ferretería Recaredo	physical	42.9400615	-6.3175673	Carretera Puerto de Cerredo- Aguilar de Campoó, 7	\N	12
1873	Fonticosur	physical	37.379782	-6.004941	\N	\N	12
1874	RedDer "La droguería"	physical	38.9792938	-0.6872921	\N	\N	12
1875	Ferrokey_3	physical	38.9790477	-0.6890134	\N	\N	12
1876	Cadena 88_3	physical	41.3679535	2.0185111	Avinguda Santa Coloma, 20, 08690, Santa Coloma de Cervelló	\N	12
1877	Delgado	physical	41.6626646	-4.7357239	\N	\N	12
1878	Ferretería Jimenez	physical	40.7036236	-3.4214671	\N	\N	12
1879	MJB Materials SL	physical	41.6348479	2.3971258	\N	\N	12
1880	Ferreteries Bosch	physical	41.671986	2.401947	\N	\N	12
1881	Keraben	physical	41.6700087	2.4014646	\N	\N	12
1882	Los Francos	physical	41.940402	-7.4420867	\N	\N	12
1883	Ferreteria Illa	physical	41.8637396	1.9714821	Plaça Major, 08279, Avinyó	\N	12
1884	La Atalaya	physical	43.4118652	-3.4137994	\N	\N	12
1885	La Broca	physical	41.4096211	2.1460339	\N	\N	12
1886	Midas	physical	41.4114808	2.1419971	\N	\N	12
1887	Andreu	physical	41.6425067	2.3968147	\N	\N	12
1888	Suministros Lama SL	physical	39.0762135	-6.0355034	Calle Argentina, 12, Conquista del Guadiana	\N	12
1889	Leroy Merlin_19	physical	36.53567	-4.6361662	\N	\N	12
1890	Jumisa	physical	40.3321692	-3.7718134	\N	\N	12
1891	Ferretería Central	physical	36.7611392	-4.0948223	Calle Julio Romero de Torres, 18-21, Vélez-Málaga	\N	12
1892	Ferretería Plácido_1	physical	36.7833241	-4.1067867	Calle Reñidero, 16, Vélez-Málaga	\N	12
1893	Ferretería Cambil	physical	37.6732974	-3.5661828	Calle Arenal, 23120, Cambil	\N	12
1894	Ferretería Juan Barruz	physical	37.6765465	-3.5658559	Calle La Tercia, 23120	\N	12
1895	Borrull	physical	41.6898985	2.4986762	\N	\N	12
1896	Ferretería Alcudia	physical	38.2918527	-0.585062	\N	\N	12
1897	Ferreteria Guayabal	physical	28.369304	-16.3642919	\N	\N	12
1898	Ferretería Liñares	physical	42.9081991	-8.7381303	\N	\N	12
1899	Ferretería San José_2	physical	40.5748233	-4.0037679	\N	\N	12
1900	Talleres Juca	physical	41.4488555	2.208374	Carrer de Francesc Moragas, 31, 08922, Santa Coloma de Gramenet	\N	12
1901	Ferretería Fegosa	physical	28.0812927	-16.7300522	Lugar Urbanización San Eugenio, 28B, 38660	\N	12
1902	Bricolaje Decoración Boñar	physical	42.8662637	-5.3222975	Calle José Fernández, 4, 24850, Boñar	\N	12
1903	Ferretería Quitet	physical	38.0924712	-0.6552357	\N	\N	12
1904	San Damián	physical	41.4440381	-5.7333938	Calle Juan de Montejo	\N	12
1905	Moreno Martín	physical	40.3867909	-5.757262	Calle Ramiro Arroyo	\N	12
1906	Castilla	physical	40.3863168	-5.7611456	Calle Libertad	\N	12
1907	Biona	physical	28.0013343	-15.5807223	\N	\N	12
1908	Ferretería Mérida	physical	37.4366565	-4.1975254	\N	\N	12
1909	Siles	physical	37.4384657	-4.1952199	\N	\N	12
1910	Ferreteria Gurri	physical	41.6893805	2.4907198	\N	\N	12
1911	Font	physical	41.6142378	2.3056827	\N	\N	12
1912	Ferretería Cristóbal	physical	37.9867655	-1.2175931	\N	\N	12
1913	Ferretería Ferre	physical	42.8473516	-8.5752812	\N	\N	12
1914	Cid	physical	42.3548316	-3.6647917	\N	https://www.ferreteriacid.es/	12
1915	Chicho	physical	43.4989716	-8.2258509	\N	\N	12
1916	Ferrobox Martínez	physical	42.0727707	-6.0150729	\N	\N	12
1917	Iru Deko	physical	43.161806	-2.7801159	Igorre	\N	12
1918	Ferretería Corona	physical	40.4031638	-3.7452673	\N	\N	12
1919	La Lonja	physical	37.5271739	-6.1561316	\N	\N	12
1920	Marlo	physical	43.3670756	-8.4098673	\N	\N	12
1921	Corplama	physical	43.5144601	-8.2207144	Estrada de Catabois, 731, 15405, Ferrol	\N	12
1922	MetolArgi	physical	43.2769381	-2.9733655	\N	\N	12
1923	El Clau	physical	41.3850009	2.1305311	\N	\N	12
1924	Ferretería Maldonado	physical	36.7213573	-4.4334258	Calle Martínez Maldonado, 17, 29007	https://ferreteriamaldonado.com/	12
1933	Elma_1	physical	40.3532763	-3.5449364	\N	http://www.sumelma.distribuidor-oficial.es	12
1934	EJMA	physical	40.4542564	-1.2862917	\N	\N	12
1935	Leñas Manel Francàs	physical	41.5741926	2.2085964	Carretera de Palaudàries a la C-155, 08185	http://www.llenyesmanel.amawebs.com/	12
1936	Ferreteria l'Espluga	physical	41.3951605	1.099866	\N	\N	12
1937	Ferreteria do Alba	physical	42.1671345	-8.7205727	\N	\N	12
1938	VivaPlanet	physical	42.6155672	-6.4187016	Calle Río Boeza, 8	\N	12
1939	Aurelio	physical	39.4844319	-0.3626566	\N	\N	12
1940	Instalaciones Moreira	physical	41.6166575	2.281495	Carrer del Prat, 26, Canovelles	https://www.instalacionesmoreira.com/	12
1941	El Orbeón	physical	36.6649329	-4.5025615	Avenida San Javier, 18, 29140	\N	12
1942	Ferreteia el Candado	physical	36.8336226	-3.9767715	\N	\N	12
1943	Ferrediaz	physical	28.4455628	-16.3093436	\N	\N	12
1944	Ferreteriala Clave, S.L.	physical	36.7482603	-3.0185888	74	\N	12
1945	Picos	physical	43.2755538	-2.9718913	Kastrexana etorbidea	\N	12
1946	Brico Encartaciones. Cadena 88	physical	43.2746243	-2.9748588	Calle Astillero / Untziola kalea, 18	\N	12
1947	Comercial Ramiro Otero	physical	42.0839953	-6.6406086	\N	\N	12
1948	Leroy Merlin_20	physical	41.6023084	2.2591146	\N	\N	12
1949	Ferreteria Oliva	physical	41.4474258	2.2126639	Carrer de les Roselles, 21, 08923	\N	12
1950	Aramburu Guzmán	physical	37.2731483	-6.9124683	Avenida virgen litoral	\N	12
1951	MultiMontseny SL	physical	41.6908443	2.4932464	\N	\N	12
1952	Femaco	physical	28.4407427	-16.314535	\N	\N	12
1953	J. Cogorro	physical	40.6278715	-4.01408	\N	http://www.jcogorro.com/	12
1954	Leroy Merlin_21	physical	41.6033068	2.2597071	\N	\N	12
1955	Bricolaje Guadalajara	physical	40.6210359	-3.2036133	\N	http://www.bricocentroguadalajara.com/	12
1956	Ferreteria FerreSuin	physical	41.6377466	2.3652788	Avinguda del Rei En Jaume, 315, 08440, Cardedeu	\N	12
1957	Ferreteria Girbau	physical	41.6416684	2.3623587	Carrer de Granollers, 17, 08440, Cardedeu	\N	12
1958	Leroy Merlin_22	physical	43.1644399	-2.6196967	\N	\N	12
1959	Sebastià Frau	physical	39.5642758	3.2070498	\N	\N	12
1961	Big Mat Cámara	physical	42.0143984	-4.5184395	Avenida de Cuba, 32(A)	\N	12
1962	Segopi	physical	42.0072646	-4.5136498	\N	\N	12
1963	Ferretería Freixeiro	physical	43.5072093	-8.1879604	Rúa Río Miño, 34, Narón	\N	12
1964	Almacenes Todo	physical	42.1538135	-7.9551076	\N	\N	12
1965	Ucanca	physical	28.0718206	-16.5556911	\N	\N	12
1966	Onix	physical	41.3980282	2.1665481	\N	\N	12
1967	Viena	physical	40.4873511	-3.3624436	\N	\N	12
1968	Ferro Almar	physical	37.3445059	-6.0455696	Calle San Isidro Labrador, 41927	\N	12
1989	Suministros Lami	physical	42.8633415	-2.7040299	\N	https://www.suministroslami.com/	12
1990	Uuzubi S.A.	physical	43.0137047	-1.9036931	\N	\N	12
1991	Ferretería Gámez	physical	37.0284956	-4.3393858	\N	\N	12
1992	Perales	physical	40.8534581	-3.61337	\N	\N	12
1993	Aralar Burdindegia	physical	42.9221484	-2.0248771	\N	\N	12
1994	Todophones	physical	28.0882387	-16.7280721	\N	\N	12
1995	Ferrocentro	physical	43.3650138	-5.8515233	\N	http://www.ferrocentro.es/	12
1996	Santana	physical	37.0280657	-4.3368181	\N	\N	12
1997	Ferretería El Puente	physical	37.0270854	-4.3369821	\N	\N	12
1998	Álvarez	physical	43.3224113	-1.9730172	Mirakruz kalea	\N	12
1999	Joica	physical	41.6172637	2.0922479	\N	\N	12
2000	J. Rocabert electric	physical	41.6172405	2.0921545	\N	\N	12
2001	Ferretería la Flecha	physical	41.6242824	-4.7747368	Calle Almendrera	\N	12
2002	Ferreteria Candau	physical	41.5338467	2.4306427	Carrer de Pablo Iglesias, 33, 08302, Mataró	https://www.ferreteriacandau.com/	12
2004	Ferreteria can fatjó	physical	41.4904362	2.0250412	Avinguda de Castellbisbal, 34, 08191, Rubí	\N	12
2020	Pintos	physical	42.5073107	-8.7632583	\N	\N	12
2021	Sánchez	physical	39.5973474	2.6786912	\N	\N	12
2022	Bahías	physical	39.4291155	2.7488721	\N	\N	12
2023	Can Costa	physical	39.5713672	3.2069523	\N	\N	12
2024	Palerm_1	physical	39.5280653	2.5059713	\N	\N	12
2025	Oleta	physical	43.2374272	-2.8799424	\N	\N	12
2026	Droguería Ángel	physical	37.3649701	-5.9685296	Barriada Nuestra Señora de la Oliva, 101, 41013, Sevilla	\N	12
2027	Ferretería Ortiz_1	physical	40.4040552	-3.6551043	Calle de la Cerámica, 88, 28038, Madrid	https://ferreteriaortiz.es	12
2028	Ferretería_13	physical	40.622308	-3.9055699	\N	\N	12
2029	Difeba	physical	39.6014098	2.6615966	\N	\N	12
2030	Socías	physical	39.6007537	2.6620233	\N	\N	12
2031	Mayol	physical	39.5711513	2.6681968	\N	\N	12
2032	Tui	physical	43.3753411	-8.3958448	\N	\N	12
2033	Marconi	physical	43.3753407	-8.3992987	\N	\N	12
2034	Luis Otaño	physical	43.3133808	-1.9014666	Biteri kalea, 23, 20100, Errenteria	https://www.ferreteriaotano.com/	12
2035	Bravo	physical	43.3664593	-8.4077865	\N	\N	12
2059	Curtiplás	physical	43.5406111	-5.6609084	\N	\N	12
2060	Quirós	physical	43.5407682	-5.6606547	\N	\N	12
2061	El Compás	physical	43.3552917	-8.4095181	\N	\N	12
2062	Todo Alquiler	physical	41.0468881	-2.6589772	Polígono Industrial Los Llanillos 3 - 5, 19250	https://todoalquiler.net	12
2063	Ferrenosa	physical	43.3534861	-8.4015386	\N	https://ferrenosa.com/	12
2064	Ferretería Uniferag	physical	40.309841	-3.8425611	\N	http://www.ferreteriauniferag.com	12
2065	Ferreteria Cantero	physical	39.7174599	-2.2201964	\N	\N	12
2066	Freijo	physical	42.5506546	-3.3228801	\N	\N	12
2073	O Prado	physical	42.3750947	-7.4161974	\N	\N	12
2074	Comercial Plasencia	physical	40.0112916	-6.1101009	Avenida Martín Palomino, 10600, Plasencia	http://www.comercialplasencia.es/	12
2075	Ferreteria Amin	physical	41.3757575	2.1237299	Carrer de Sants, 346, 08028, Barcelona	\N	12
2076	Comercial Freire e Núñez	physical	42.5749512	-9.0717447	\N	\N	12
2077	BIGMAT. Ismael Tello,SA	physical	39.1477302	-5.9133961	\N	\N	12
2098	Terra Chá	physical	43.2355598	-7.5580394	\N	\N	12
2099	Reloxería Manuel	physical	43.1254559	-7.0702463	\N	\N	12
2100	Ferretería Mateo	physical	37.0244155	-3.626344	Calle Escuelas, 18640	\N	12
2101	Ferreteria Cenit	physical	37.0246203	-3.6229558	Calle Prado, 18640	\N	12
2102	Repuestos los llanos	physical	37.8183876	-5.0073794	Carretera de Palma del Río, 14720, Almodóvar del Río	\N	12
2103	Torres III	physical	39.5729813	-0.32685	\N	\N	12
2104	Hermanos galende	physical	41.999896	-6.016255	\N	\N	12
2105	Ferretería Industrial Díaz Hellín	physical	39.308854	-3.031726	\N	\N	12
2106	Sánchez Quintanar	physical	39.4013469	-3.1165284	\N	\N	12
2107	Suministros Amador	physical	39.3980991	-3.1279922	\N	\N	12
2108	Ferretería Arenal_2	physical	39.4055086	-3.1224883	\N	\N	12
2112	La llave	physical	42.5866004	-5.5670691	Avenida de Fernández Ladreda	\N	12
2113	Ferretería Bisal	physical	42.0890291	-8.4191189	\N	\N	12
2114	Ferretería Bisal_1	physical	42.0890413	-8.4191123	Rúa Entrecines	\N	12
2115	Cerámica Josep Torres	physical	41.9651639	3.034547	\N	\N	12
2116	Ferretería Maracay	physical	42.1949214	-8.6498463	\N	\N	12
2117	Ferretería El Gallego	physical	42.5944145	-4.3303381	Plaza de Santa Ana, 34400, Herrera de Pisuerga	\N	12
2118	New Brico	physical	38.0930037	-1.7837864	Ronda Este, 30430, Cehegín	\N	12
2119	Freire	physical	43.3572159	-8.4152486	\N	\N	12
2120	Badysat	physical	43.4690547	-3.802898	Calle de Fernando de los Ríos, 62, 39006, Santander	https://www.badysat.com/	12
2121	Indufer	physical	43.3236707	-2.9881612	\N	\N	12
2152	Ferretería Roberto_1	physical	41.6627689	-4.7224946	\N	\N	12
2187	Couselo	physical	43.0754318	-8.4081679	\N	\N	12
2188	A Tenda de Darío	physical	43.2332602	-8.2829688	O Penedo, Mabegondo, 45, 15318, Abegondo	\N	12
2189	Ferretería La Llave_1	physical	43.2175994	-6.8766338	\N	\N	12
2190	Ferretería Luisín	physical	43.2185304	-6.874859	\N	\N	12
2191	Ferreteria la nova	physical	41.3898718	1.9368131	Carrer Major, 169, 08759, Vallirana	\N	12
2192	Ferretería Antón	physical	40.6273354	-4.01165	\N	\N	12
2193	González Ruano	physical	40.4086926	-3.6695729	Calle de Lira, 1, 28007, Madrid	\N	12
2194	Valcárcel	physical	42.7264731	-7.0217522	\N	\N	12
2195	El Mirador	physical	43.3530791	-8.3905079	\N	\N	12
2196	Ferretería de Marcenado	physical	40.4457487	-3.6727276	Calle de Marcenado, 8, 28002, Madrid	\N	12
2197	Enrique Vázquez	physical	43.4824168	-8.2360085	Rúa Madalena, 180, 15402, Ferrol	https://enriquevazquez.es/	12
2198	Ferretería Piolo	physical	38.3708714	-0.4125287	Avenida de Bruselas, 6	\N	12
2199	Garau	physical	39.7641418	3.1615815	Carrer Isabel Garau Ribas, 27, 07458, Can Picafort	\N	12
2298	Ferretería Jiménez_1	physical	39.2093108	-1.7247994	\N	\N	12
2047	Decormad	physical	40.6338669	-4.0066718	\N	\N	12
2048	Fervi	physical	39.5895671	2.6793852	\N	\N	12
2049	Encuentra	physical	37.8826491	-4.7939431	Gran Vía Parque, 21, 14005, Córdoba	http://www.encuentraferreteria.com/	12
2050	Hércules	physical	43.3787867	-8.4047172	\N	\N	12
2051	La Casilla	physical	43.2580291	-2.9469504	Calle Autonomía / Autonomia kalea, Bilbao	\N	12
2052	Can Ferrer	physical	39.582682	2.6738972	\N	\N	12
2053	Provibuques	physical	43.3961571	-3.4602622	\N	\N	12
2054	Adarra	physical	43.2675698	-1.9751951	\N	\N	12
2055	Ferretería Ortez	physical	40.6275731	-4.0080133	\N	\N	12
2056	Seriland	physical	43.2445422	-8.2753861	Ferrería, Mabegondo, 15318, Abegondo	\N	12
2057	Ferretería A. Rubio	physical	40.7421247	-4.0541056	\N	\N	12
2058	Mafonsa	physical	42.1057779	2.7861543	Carrer Indústria	\N	12
2067	Comercial Ferretería Ima	physical	41.6284666	-4.7424771	\N	\N	12
2068	Ferretería Cabrera García	physical	28.1460652	-15.650166	\N	\N	12
2069	Ferretería Padrón	physical	28.1457315	-15.6559528	\N	\N	12
2070	Ferretería D.S	physical	28.1453039	-15.6512099	\N	\N	12
2071	Fernández	physical	42.0610749	-7.1374712	\N	\N	12
2072	Suministros Arriaga	physical	42.8436144	-2.7408715	\N	\N	12
2078	Molduras Ruiz	physical	36.8349429	-3.9748002	Avenida de Canillas, 29754, Cómpeta	\N	12
2079	Maype Ferretería Pinturas	physical	43.4688334	-3.7980519	Calle de la Virgen del Camino, 4, 39006, Santander	\N	12
2080	Comercial Naval Canaria	physical	28.1503515	-15.4197663	\N	\N	12
2081	La Ferretería_3	physical	42.8448094	-2.6843441	Abendaño, 21	\N	12
2082	Apezteguia	physical	43.1334576	-1.6762749	\N	\N	12
2083	Brico Jaca	physical	42.5612159	-0.5054164	\N	\N	12
2084	Bricobalears	physical	39.8433495	3.1320315	\N	\N	12
2085	Carpintería Betiko S.I	physical	43.1799241	-1.4882974	\N	\N	12
2086	Ferreteria_8	physical	42.4757187	-7.9860226	\N	\N	12
2087	Nueva Hidroneumática Canarias	physical	28.1506534	-15.42002	\N	\N	12
2088	Tesol Canarias	physical	28.1505273	-15.420162	\N	\N	12
2089	La Naval Ferretería	physical	28.1505194	-15.4209177	\N	\N	12
2090	José Herrero	physical	28.1499518	-15.4234717	\N	\N	12
2091	Pinturas Moisés Gil	physical	28.150319	-15.4241533	\N	\N	12
2092	Teinsa Tecnomecánica	physical	28.1498469	-15.4263101	\N	\N	12
2093	Midisa 2000	physical	28.1495425	-15.4274605	\N	\N	12
2094	Würth_5	physical	40.6282809	-4.0184336	\N	\N	12
2095	Hiperconstrucción Ferretería Ruiz	physical	40.6281001	-4.0194853	\N	\N	12
2096	Ferreteria Puig	physical	42.1693928	2.4756742	\N	\N	12
2097	Mañó Mascarell	physical	38.966217	-0.1908903	Carrer Ciutat de Barcelona, 23, 46702, Gandia	\N	12
2109	Ferretería Rada	physical	39.5578578	-2.7054947	\N	\N	12
2110	Ferretería Vulcano	physical	36.7024643	-4.4420776	Calle Héroe de Sostoa, 145, 29003	\N	12
2111	Suministros Nerva	physical	37.6962905	-6.5500788	\N	\N	12
2122	Pere Joan	physical	42.1712959	3.0747541	\N	\N	12
2123	Ferretería Monforte	physical	38.378993	-0.7317471	Avenida de Aspe, 25	\N	12
2124	Ferretería Avenida_3	physical	38.5376161	-0.1186646	Calle de Gerona, Benidorm	\N	12
2125	Ferrobox_1	physical	43.216397	-3.8069154	\N	\N	12
2126	Cadena88	physical	43.2154144	-3.8059565	\N	\N	12
2127	Aceiro	physical	43.3531965	-8.4148465	\N	\N	12
2128	Comercial Talleres Electrón	physical	42.5556047	-5.5503257	\N	https://www.grupoelectron.com/	12
2129	Becani	physical	43.2694389	-8.2246008	\N	\N	12
2130	Castañer	physical	41.9574244	2.6435511	\N	\N	12
2131	Ferretería Font	physical	38.5399781	-0.1304977	Avenida de Ruzafa - Avinguda de Russafa, 49, 03501, Benidorm	\N	12
2132	La Muralla	physical	40.3296772	-3.8673847	Calle Pintor Ribera posterior, 1, 28933, Móstoles	\N	12
2133	Talleres Sáez	physical	41.2348941	-0.0463473	Calle Diputación, 23, 50700, Caspe	\N	12
2134	BigMat_3	physical	42.8561422	-4.498801	\N	\N	12
2135	Carnero	physical	42.5871716	-5.5613872	Avenida de Fernández Ladreda	\N	12
2136	Leroy Merlin_23	physical	37.2848434	-5.9392315	\N	\N	12
2137	Suministros Ferpa	physical	43.6650403	-7.5928658	\N	\N	12
2138	Grandío	physical	43.3493085	-8.3965894	\N	\N	12
2139	Ferreteria Moreno	physical	40.0095928	-3.0129137	\N	\N	12
2140	La Ferretería_4	physical	38.5388781	-0.1085893	Avinguda de Juan Fuster Zaragoza, 10, 03503, Benidorm	\N	12
2141	Leal	physical	43.3175312	-2.9842127	Calle Consulado de Bilbao	\N	12
2142	Ferraxería A Calzada	physical	43.1363149	-8.3174208	A Calzada, Visantoña, 15689, Mesía	\N	12
2143	Maryant	physical	41.4013364	2.2031586	\N	\N	12
2144	Ferretería Avenida_4	physical	41.4031215	-4.3094926	Avenida de la Plaza de Toros, 5, 40200, Cuéllar	\N	12
2145	Sánchez_1	physical	43.1524429	-8.3806087	\N	\N	12
2146	Bosch	physical	41.9569659	2.6422039	\N	\N	12
2147	Ferretería Serafín	physical	43.1613448	-7.8405596	\N	\N	12
2148	Ferreteria Carmona	physical	41.4486775	1.9724974	Carrer de la Riera de Canals, 9, 08740, Sant Andreu de la Barca	\N	12
2149	Optimus La Roda	physical	41.4479601	1.9725107	\N	\N	12
2150	Milla	physical	43.2968654	-2.9922102	\N	\N	12
2151	Neira	physical	43.2952461	-2.997364	\N	\N	12
2153	Ferretería Magar	physical	40.4697261	-3.8739858	Calle Luna, 7, 28220, Majadahonda	https://www.ferreteriamagar.es/	12
2154	Leroy Merlin_24	physical	37.7901047	-3.7731709	Carretera de Bailén a Motril, Jaén	https://www.leroymerlin.es/tiendas/jaen	12
2155	Montaña	physical	43.2806788	-2.9837948	\N	\N	12
2156	Montaña_1	physical	43.280215	-2.9833768	Calle Vista Alegre kalea	\N	12
2157	Comercial Urnisa	physical	42.3448233	-3.6877839	\N	https://www.urnisa.com/	12
2158	Ferretería Estepa	physical	37.5716053	-5.4295057	\N	\N	12
2159	Ferretería Gómez e Hijos S.L	physical	37.567893	-5.4273627	\N	\N	12
2160	Comercial Moncho	physical	42.7195633	-8.6503256	\N	\N	12
2161	Cántabra de Electricidad	physical	43.4553472	-3.815296	\N	\N	12
2162	Bazar-Ferretería Casa Rita	physical	38.2759859	-6.9190381	\N	\N	12
2163	Comercial Fructuoso	physical	38.2771797	-6.9215144	\N	\N	12
2164	Multicentro de Ferretería, Jardinería y Maquinaria Rome	physical	40.4444914	-3.4655791	Carretera de Loeches, 84	https://www.gruporome.com/	12
2165	Instaladora La Naval	physical	28.149589	-15.4297227	\N	\N	12
2166	Electrónica Tecén	physical	28.1512508	-15.4235707	\N	\N	12
2167	MSM Rodamientos	physical	28.1505649	-15.4264757	\N	\N	12
2168	Ferreteria J. Farreny	physical	41.3961267	2.1541828	Carrer del Comte de Salvatierra, 2	\N	12
3101	Paulino López	physical	\N	\N	\N	\N	12
2169	Ferretería Barrios	physical	41.6622362	-4.7208312	Calle de las Moradas, 29, 47010, Valladolid	\N	12
2170	Pulygal S.L.	physical	40.4025858	-3.6909913	Calle del General Lacy, 28, 28045, Madrid	\N	12
2171	Montejo	physical	43.1691169	-2.6357609	Askatasun etorbidea	\N	12
2172	Campins	physical	39.5546747	2.7780467	\N	\N	12
2173	Paradise	physical	40.504603	-3.5077185	Avenida de Valdediego, 10, 28860, Paracuellos de Jarama	\N	12
2174	Ferretería Vulcano_1	physical	36.7215936	-4.4307864	Calle Mármoles, 60	\N	12
2175	Ferretería Contador	physical	38.5166506	-6.8488848	\N	\N	12
2176	Bricocaspe	physical	41.2330658	-0.0402042	Avenida Joaquín Costa, 39, 50700, Caspe	http://bricocaspe.es/	12
2177	BdB Gasca	physical	41.2335527	-0.0421217	Avenida Joaquín Costa, 18, 50700, Caspe	https://materialesgasca.es/	12
2178	Cristalería Arona	physical	28.3571298	-16.7121412	\N	https://www.cristaleriarona.com/	12
2179	Eurodal	physical	42.6462519	-8.8841396	\N	\N	12
2180	Ferreteria Masi	physical	39.5372325	-0.3716229	\N	\N	12
2181	Repuestos San Cristóbal	physical	38.2835256	-6.9153241	\N	\N	12
2182	Brico Cash	physical	38.2843029	-6.9144919	\N	\N	12
2183	Jesús	physical	36.3413052	-6.0950747	\N	\N	12
2184	Sánchez_2	physical	36.3389997	-6.0932161	\N	\N	12
2185	Ferretería Marqués	physical	42.6205419	-6.6375084	\N	\N	12
2186	Mikeldi	physical	43.1693029	-2.6169505	\N	\N	12
2200	T.M.O.	physical	40.4563003	-3.679987	\N	\N	12
2201	Electro Molina	physical	41.6383735	2.1616576	\N	\N	12
2202	La Flota	physical	37.9951187	-1.1232692	\N	\N	12
2203	Tableros al Corte - Bricolage	physical	40.5620986	-4.0160695	\N	\N	12
2204	Bricotech	physical	41.6378478	2.3678478	Avinguda del Rei En Jaume, 345, 08440, Cardedeu	\N	12
2205	BigMat_4	physical	40.5533655	-4.0212735	\N	\N	12
2206	Ferretería Alicante	physical	43.3511738	-8.3937291	\N	\N	12
2207	Ferretería Hernanz	physical	40.4480247	-3.673513	\N	\N	12
2208	Cespeval	physical	39.5673523	-0.505021	\N	\N	12
2209	Decolor	physical	39.5739127	2.7173575	\N	\N	12
2210	Bricolaje Juan	physical	40.0299479	-3.606256	\N	\N	12
2211	Decoplus	physical	40.0306005	-3.6062054	Calle de la Florida, 57	\N	12
2212	Bonaire	physical	38.7191121	0.0610954	\N	\N	12
2213	Ferretería El Bombín	physical	37.4047035	-5.9755082	\N	\N	12
2214	Shermacon	physical	40.6250827	-4.0257721	\N	https://www.shermacon.com/	12
2215	Ferretería_14	physical	40.6250961	-4.0240145	\N	\N	12
2216	La Confiteria	physical	39.7582653	-4.9492933	\N	\N	12
2217	SeySu Hidráulica	physical	40.6301326	-4.0206534	\N	\N	12
2218	La Palloza	physical	43.3579379	-8.4029573	\N	\N	12
2219	Tot Útil	physical	38.7380899	-0.0085945	\N	\N	12
2220	Santos	physical	38.7411781	-0.0132474	\N	\N	12
2221	Sonitel Noroeste	physical	43.3522084	-8.391269	\N	\N	12
2222	Ugao	physical	43.1812835	-2.9013859	\N	\N	12
2223	Würth Collado Villalba	physical	40.6282833	-4.01844	\N	https://www.wurth.es	12
2224	Ferreteria Montseny	physical	41.637567	2.3584898	Carrer del Montseny, 20, 08440, Cardedeu	https://ferreteriamontseny.cat/	12
2225	Ferretería San Jorge	physical	42.1387221	-0.4151258	Calle de la Jota Aragonesa, 10	\N	12
2226	Manolo	physical	43.2751655	-1.6884902	\N	\N	12
2227	Ferretería M. Ortez	physical	40.6270945	-4.0201205	\N	\N	12
2228	Bricofer_1	physical	38.54521	-0.1330262	Avinguda de Beniardà, Benidorm	\N	12
2229	Ferretería Séneca	physical	37.1801058	-3.6126635	Calle Séneca, 7, 18003, Granada	\N	12
2230	Ferretería Costa Blanca	physical	38.537788	-0.1311241	Carrer de Tomás Ortuño, 17, Benidorm	\N	12
2231	Hijos de juan Ribes	physical	38.7165254	0.0593989	\N	\N	12
2232	Ferretería La Cerradura	physical	40.9728133	-5.651658	\N	\N	12
2233	Comercial Fontan	physical	43.3043082	-8.5114252	\N	\N	12
2234	El Tucan	physical	41.3870686	2.13789	Carrer del Berguedà, 7, 08029, Barcelona	https://eltucan.es	12
2235	Ferretería Julián Herrero	physical	40.3577479	-5.5235283	Calle de Santa Teresa, 7, 05600, El Barco de Ávila	\N	12
2236	Daniel Saneamientos	physical	40.9700002	-5.6652766	\N	\N	12
2237	Ferretería Aljarafe	physical	37.3488456	-6.0428195	\N	\N	12
2238	Ferretería Chacón	physical	40.950022	-5.6287859	\N	\N	12
2266	Ferretería Vila de Cambre	physical	43.2927809	-8.3431472	Estrada Cambre-O Temple, 4, 15660, Cambre	https://www.ferreteriaviladecambre.es/	12
2267	Ferretería Gaucín	physical	36.6979945	-4.4487934	\N	\N	12
2268	Ferretería Bardán	physical	36.6995344	-4.4511341	\N	\N	12
2276	Prodesco	physical	39.490319	-0.4672087	Calle de la Aviación	\N	12
2277	Prodesco_1	physical	39.4903153	-0.4672548	Calle de la Aviación, 44, 46940	https://prodesco.es/	12
2278	Ferretería Iñigo	physical	43.2191887	-2.7295672	San Juan kalea, 10, 48340, Amorebieta-Etxano	\N	12
2279	Ferretería la Vega	physical	43.3346383	-4.9705227	Benia de Onís	\N	12
2280	Ferretería Zornotza	physical	43.219331	-2.7320524	San Migel kalea, 14, 48340, Amorebieta-Etxano	http://ferreteriazornotza.com/	12
2281	Carmona	physical	38.8895141	-3.7098727	\N	\N	12
2282	Ferretería El Resiste	physical	42.8657099	-4.4980282	\N	\N	12
2283	Orellana	physical	39.5122601	-0.4155649	Calle de Rubert y Villo, 7, 46100, Burjassot	\N	12
2284	Ferretería Ademuz	physical	40.0637972	-1.2852272	Avenida Valencia, 130, 46140, Ademuz	https://www.ferreteriaademuz.com/	12
2285	Almaproin S.A.	physical	40.4024929	-3.6768381	Avenida de la Ciudad de Barcelona, 57	https://www.almaproin.com	12
2286	Ferretería Burgalesa	physical	42.3524018	-3.6612374	\N	\N	12
2287	Ferreteria Baró	physical	41.6309266	0.8951547	Carrer del President Macià, 13, 25230, Mollerussa	http://www.ferreteriabaro.com/	12
2288	Saneamientos José Gómez	physical	36.8460269	-2.4411598	\N	\N	12
2289	Menaje Hogar	physical	42.6451098	-8.8905608	\N	\N	12
2290	Casais	physical	42.646361	-8.8829373	\N	\N	12
2291	BigMat_5	physical	41.5209757	0.8656455	\N	\N	12
2292	Nic Optimus - Ferreteria	physical	41.5169667	0.874624	Avinguda de Francesc Macià, 1, 25400, les Borges Blanques	https://www.laclauferreteria.com/	12
2293	Fernanz	physical	41.4044647	-4.306743	\N	\N	12
2294	Ferretería Olaguibel	physical	42.8448985	-2.665663	Pio XII.aren kalea/Calle Pío XII, 15, 01004, Vitoria-Gasteiz	https://ferreteriaolaguibel.wordpress.com/	12
2295	Jauregui Katxarritos	physical	42.8473147	-2.6699068	San Frantzisko kalea/Calle San Francisco, 5, 01001, Vitoria-Gasteiz	https://katxarritos.com/	12
2296	Visanfer	physical	37.8474738	-1.4234081	\N	https://www.visanfer.com/alhama	12
2297	Ferroabeca	physical	37.8505253	-1.4212107	\N	\N	12
2239	Ferretería Los Pinos_1	physical	38.5380934	-0.1237446	Carrer de Girona - Calle de Gerona, Benidorm	\N	12
2240	Diyesca Ferrol	physical	43.5147203	-8.2195735	\N	http://diyesca.es/	12
2241	Manuel Vázquez Pérez. S.L.	physical	43.5131029	-8.2181962	\N	https://www.grupomvp.com	12
2242	Ferretería El Carmen_1	physical	39.2761635	-0.2756296	\N	https://www.cadena88.com/es	12
2243	BeckFloor	physical	40.4565879	-3.6964676	\N	\N	12
2244	Diego Cabrera	physical	38.7257474	0.0744429	N-332, Benissa	https://www.materialesdiegocabrera.com/	12
2245	Recambios Freire	physical	42.8757785	-7.8643684	\N	\N	12
2246	Garsal	physical	38.7162375	0.0568972	\N	\N	12
2247	Ausina - Maderas	physical	38.7171394	0.0574487	\N	\N	12
2248	Can Xic_1	physical	39.6177668	2.771023	\N	\N	12
2249	Agroindustrial Ridao	physical	37.0016403	-1.8913669	Calle San Fernando, Carboneras	\N	12
2250	El Clau Tort	physical	39.4635888	-0.4608351	Carrer Reis Catòlics, 27, 46960, Aldaia	\N	12
2251	Ferretería Plaza	physical	42.2250232	-8.7524549	Pescadores, 10, 36208, Vigo	\N	12
2252	Ferreteria Pedro Pinto	physical	36.926932	-4.5914054	\N	\N	12
2253	Ferretería Novo Llavín	physical	36.7809929	-4.106559	\N	\N	12
2254	Cano_1	physical	39.5595489	2.898461	\N	\N	12
2255	Laclau	physical	38.8738656	-0.7519928	\N	\N	12
2256	Ferretería Cerdá	physical	37.1831219	-1.821286	Calle Mayor, 76, 04630, Garrucha	\N	12
2257	Sáez	physical	40.4559104	-3.7046031	\N	\N	12
2258	Ferretería Jupe	physical	40.3185648	-3.7237006	28903, Getafe	\N	12
2259	Tornillería A Ría	physical	43.245867	-8.3571174	\N	https://www.suministros-ria.com/	12
2260	Ferretería Octavio	physical	38.5214203	-3.5640294	\N	\N	12
2261	Salomón	physical	42.9114474	-8.7369472	\N	\N	12
2262	Comercial Distribuidora Muñoz	physical	37.0252684	-4.3341986	Calle del Barbate, 29313, Villanueva del Trabuco	\N	12
2263	Ferretería Piélagos	physical	43.3519268	-3.9512867	Avenida de Aurelio Diez, 8, 39470, Renedo de Piélagos	\N	12
2264	Fariñas	physical	37.2614235	-6.9377054	\N	\N	12
2265	Todo en Gloria	physical	37.1836561	-1.8208723	Calle Mayor, 04630, Garrucha	\N	12
2269	Ferreteria Morelló	physical	42.7013167	0.7945363	\N	\N	12
2270	Sumitor - Suministros industriales	physical	40.3985137	-3.7171588	Calle Pablo Montesinos, 5, 28019, Madrid	http://www.sumitorsuministros.com/	12
2271	Leroy Merlin_25	physical	41.3876338	2.1722409	Carrer de Fontanella, 12	https://leroymerlin.es	12
2272	Cadena 88 Ferretería	physical	38.1967788	-0.5613706	Carretera d'Elx-Santa Pola / Carretera de Elche-Santa Pola, 5	https://ferreterias.cadena88.com/tiendas/brico-pinturas-dami	12
2273	Plaza China	physical	40.3503165	-3.6920372	Calle de Santa Petronila, 13, 15, 28021	\N	12
2274	Hiper Porto Cristo	physical	39.5455701	3.331666	\N	\N	12
2275	Comercial Palmer	physical	39.3752053	3.2281399	\N	\N	12
2318	Suministros Aguadulce	physical	37.252562	-4.9917402	Calle San Bartolomé, 10, 41550, Aguadulce	\N	12
2319	Nf Bricolaje	physical	43.5259798	-5.6752336	\N	\N	12
2320	Ferro	physical	40.4289997	-3.6052323	\N	\N	12
2321	Ferretería Arrate Ezquerra	physical	43.1022332	-3.279903	Calle Doctor Eladio Bustamante Peña, 35	\N	12
2322	Ferretería La Garrucha	physical	37.1865067	-1.8198453	Calle Mayor, 04630	\N	12
2323	Ferretería Villalón	physical	36.5112081	-4.8887362	\N	\N	12
2324	Copalma	physical	28.8022182	-17.7732529	\N	\N	12
2325	Ferconsa	physical	28.8015886	-17.7726842	\N	\N	12
2326	La Comarca Ganollers	physical	41.604826	2.2855923	Carrer Sant Jaume, 102	\N	12
2327	Ferreteria de la Muñoza	physical	41.54508	2.2080988	Carrer de Sant Andreu, 21, 08100, Mollet del Vallès	https://ferreteriadelamunoza.com/ca	12
2328	Ferretería Agrocentro	physical	38.1182932	-3.0813707	\N	\N	12
2329	Ferretería Campos	physical	38.1187848	-3.0789581	Avenida Gómez de Llano, 57	https://www.ferreteriacampos.es/	12
2330	Cuchillería Manolo	physical	40.9721304	-5.6610467	Avenida de Portugal, 96, Salamanca	\N	12
2331	Ferretería Catalunya	physical	41.3585944	2.0736438	Carrer de Catalunya, 08940, Cornellà de Llobregat	\N	12
2332	Aller	physical	41.6585528	-4.7190483	Calle Real de Burgos, 11, 47011, Valladolid	\N	12
2333	Es Brico	physical	38.936216	1.4163819	\N	\N	12
2334	Ferretería Bejerano	physical	40.6567168	-4.0963516	\N	\N	12
2335	Suministros Santovenia	physical	41.5874173	-4.5823713	\N	\N	12
2336	Ferretería Azorín	physical	37.1719068	-3.6075714	Calle Buenos Aires, 9, 18004, Granada	\N	12
2337	Ferreteria Industrial Lualdasa	physical	40.2287262	-3.7810978	Viario de Ronda, 28980, Parla	\N	12
2338	Obramat_1	physical	38.5349221	-0.1813141	\N	https://www.bricomart.es	12
2339	Duchas Inox	physical	41.4528521	1.9705306	Passatge de Màlaga, 2-4, 08740, Sant Andreu de la Barca	https://duchasinox.com	12
2340	El Arco	physical	41.6410402	-4.73166	\N	\N	12
2341	Ferreteria Puerto	physical	28.2391855	-16.8404434	\N	\N	12
2342	Malumar's	physical	43.5406198	-5.6993611	Calle Brasil, 20	\N	12
2343	Fuente el Sol_1	physical	41.6626411	-4.7355853	\N	\N	12
2344	Würth_6	physical	28.0950848	-17.1139272	\N	\N	12
2345	Ferreteria Sanchez	physical	28.0955902	-17.1146463	\N	\N	12
2347	EUROCOBEL 98	physical	40.3757517	-3.6437588	Calle de Luis I, 31	\N	12
2348	Aisa Floor	physical	40.4592518	-3.7075282	\N	\N	12
2349	Ferreteria Martí	physical	41.1556567	1.1118729	Plaça Puríssima Sang, 1, 43201, Reus	\N	12
2350	Ferretería Milín	physical	37.1440234	-3.5715579	\N	\N	12
2351	Equipos de Descanso De Domingo	physical	40.4586066	-3.7002641	\N	\N	12
2352	Ferretería Enol / Ferrokey	physical	40.3881273	-3.7402678	\N	\N	12
2353	Ferretería Tetuán	physical	40.4592795	-3.6992967	\N	\N	12
2354	La ferretería de Nicolás	physical	37.3451231	-5.9823726	Avenida de Alemania, 13, 41012, Sevilla	\N	12
2355	Ferretería Alhamar	physical	37.1689104	-3.6031453	Calle Alhamar	\N	12
2356	El Curro	physical	37.1520961	-3.5813642	\N	\N	12
2357	Puente Verde	physical	37.1518996	-3.5807914	\N	\N	12
2372	Ferretería Fergal	physical	40.392521	-3.7554943	\N	\N	12
2373	Ferretería Loan	physical	40.3938187	-3.7632563	\N	\N	12
2374	Ramis Stock	physical	38.840024	0.0991652	\N	\N	12
2375	Hiper	physical	40.3001744	-4.4370803	\N	\N	12
2376	Ferretería Ferba	physical	39.5793088	-0.3455372	Carrer de Bonaire, 3, 46130, Massamagrell	https://ferreteriaferba.com/	12
2396	Stihl	physical	42.1644762	0.8931533	Carrer de Tarragona, 12, 25620, Tremp	\N	12
2397	Ferretería Provenza	physical	41.3895453	2.1548253	\N	\N	12
2434	Ferretería Salomea	physical	37.678486	-6.6602917	\N	\N	12
2299	Bricoferre Cadena 88 Ferreterías	physical	40.0627452	-5.7532374	Avenida de la Constitución, 8	https://ferreterias.cadena88.com/tiendas/bricoferre	12
2300	IMPEX Subministres SL	physical	42.1152532	3.1259395	\N	\N	12
2301	Moix	physical	41.3960435	2.1436894	\N	\N	12
2302	Víctor	physical	43.3091782	-3.0052263	\N	\N	12
2303	BricoThiviers	physical	38.7904805	0.1679818	Calle Juan Ramón Jiménez, 17, 03730	\N	12
2304	Ferretería Jesús Utrera	physical	37.7656586	-3.7912562	Calle Maestra, 5, 23002	http://www.cadena88.com	12
2305	Garau_1	physical	39.7049203	3.1061588	\N	\N	12
2306	Ferretería Industrial Munuera	physical	37.851311	-1.417705	\N	\N	12
2307	AEP Mantenimiento e Instalaciones	physical	40.4693616	-3.6870883	\N	\N	12
2308	Hidràulica i Pneumàtica Lleidatana, SL	physical	41.6275373	0.6246605	Carrer de les Corts Catalanes, 54, 25005, Lleida	\N	12
2309	Ferretería Ferrolar	physical	43.2336887	-8.6796062	\N	\N	12
2310	Ferretería La Prensa	physical	40.3761955	-3.7442333	\N	\N	12
2311	Ferretería Olaguibel Burdindegia	physical	42.8449631	-2.6656568	Pio XII.aren kalea/Calle Pío XII, 15	https://ferreteriaolaguibel.wordpress.com	12
2312	Torres_2	physical	28.1617695	-14.2303352	\N	\N	12
2313	Mateos - Rebollo	physical	39.4750604	-6.373118	\N	\N	12
2314	Aldaba	physical	43.5365213	-5.6621126	\N	\N	12
2315	Herramientas Bazarot	physical	37.3746403	-5.9255761	Calle Pino Ponderosa, 15, 41016, Sevilla	https://herramientasbazarot.com/	12
2316	El Palais	physical	43.3683419	-5.8238	\N	\N	12
2317	Jalema	physical	41.5196465	1.9001312	\N	\N	12
2346	Eloy.cab	physical	41.658621	-4.7201035	\N	https://www.ferreteriaeloycab.es/	12
2358	Cadena 88_4	physical	37.1655667	-3.5941607	Calle Poeta Manuel de Góngora, 17	https://www.cadena88.com/es/store/fernando	12
2359	Ferretería Hípica Puente Verde	physical	37.1668477	-3.5900544	\N	\N	12
2360	Ferreterías Esperidón	physical	37.1700229	-3.5986051	\N	\N	12
2361	Ferretería G 99	physical	37.7433556	-2.5542715	Calle Cervantes, 18840, Galera	\N	12
2362	Ferretería Cervantes	physical	37.1629567	-3.5869429	\N	\N	12
2363	Llomgar	physical	39.8510797	3.1262987	\N	\N	12
2364	Ferrecal	physical	42.9130937	-8.5058728	Vía de Arquímedes, 1, Santiago de Compostela	https://ferrecal.com	12
2365	Ferrecal_1	physical	43.3550632	-8.4254247	Rúa Juan de la Cierva, 11, A Coruña	https://ferrecal.com	12
2366	Ferretería Las Castillas	physical	40.690661	-3.3691045	\N	http://www.ferreterialascastillas.com/index.asp	12
2367	Multiservicios Miguel García Alcalde	physical	37.1632026	-3.5878912	\N	\N	12
2368	Cristalerías Reformas	physical	40.3865527	-3.7582498	\N	\N	12
2369	Pavisuelos	physical	37.1622811	-3.5964852	\N	\N	12
2370	Ferretería Vergeles	physical	37.162974	-3.5964434	\N	\N	12
2371	Heycor	physical	36.7378844	-3.512628	\N	\N	12
2377	Suministros Industriales Arnaldos, S.L.	physical	38.0442109	-1.2368535	N-344, KM 8,5, 30565, Las Torres de Cotillas	https://siasuministros.com/	12
2378	Ferretería Avenida_5	physical	38.0219097	-1.2373302	Avenida de los Pulpites, 2, 30565, Las Torres de Cotillas	https://www.cadena88.com/es	12
2379	Sumidecant	physical	43.3972474	-3.8386608	Parque empresarial de Morero, 10, 39611, Guarnizo	https://sumidecant.es	12
2380	Es Camp	physical	39.695638	2.7005721	\N	\N	12
2381	Ferretería_15	physical	37.2865047	-5.9114049	\N	\N	12
2382	Ferretería Navacerrada	physical	40.7302976	-4.01418	Calle de la Iglesia, 12, 28491, Navacerrada	http://www.cadena88.com/navacerrada	12
2383	Ferreben	physical	36.5937532	-4.5729802	\N	\N	12
2384	Ferretería_16	physical	40.3890772	-3.7613946	\N	\N	12
2385	Ferretería Plaza_1	physical	41.6498388	-4.7140974	\N	\N	12
2386	Ferretería Julià Lledó	physical	39.5722771	-0.3341827	\N	\N	12
2387	Bazar Ruan	physical	40.3926631	-3.709392	\N	\N	12
2388	Coloma 2	physical	38.8396303	0.0997069	\N	\N	12
2389	Ferretería del Oso	physical	40.5918247	-4.146263	\N	\N	12
2390	Obramat_2	physical	41.5633922	2.0361425	Avinguda del Vallès, 484-490, 08227, Terrassa	https://www.obramat.es/nuestros-almacenes/bm-terrassa.html	12
2391	SUMINISTROS INDUSTRIALES ARIZTIMUÑO S.L.	physical	43.2135506	-2.0231192	\N	\N	12
2392	Ferreteria Gorostidi Burdindegia	physical	43.2185848	-2.0202397	\N	\N	12
2393	Ferreteria Elizondo	physical	43.2197658	-2.0195662	\N	\N	12
2394	Ferretería El Pino Electricidad	physical	36.7307272	-3.9615899	Avenida de Andalucía, 18, 29793, Torrox-Costa	\N	12
2395	Ferreteria Leo	physical	41.3731222	2.1423276	08014, Barcelona	\N	12
2410	Comercial Baute	physical	28.3732195	-16.7653776	\N	\N	12
2411	Sleazy Records	physical	36.7249512	-4.4206364	Calle Dos Aceras, 14, 29012, Málaga	http://www.sleazyrecords.com/	12
2412	Ferretería La Caleta	physical	37.1863464	-3.6106602	\N	\N	12
2413	Ferreteria Vivet Cadena 88	physical	41.874091	2.2872797	\N	\N	12
2414	Würth_7	physical	39.7123743	2.9025281	\N	\N	12
2415	Cerrajería Hermanos Puntas	physical	37.883165	-4.7812471	\N	\N	12
2416	Electrodomésticos Milar. Todo a 100.	physical	42.423434	-2.0795421	Calle Frontón, 6, 31580, Lodosa	\N	12
2417	Arbiol	physical	41.6316434	-0.8877454	\N	\N	12
2418	Ferretería del Porvenir	physical	37.3719535	-5.9825781	\N	\N	12
2419	Maderas Santana (Ferretería Taco)	physical	28.4458919	-16.3002479	Calle Nuevo Mundo, 2, 38107, Taco	https://maderassantana.com	12
2420	Bolibar ferreteria	physical	41.3899656	2.1645449	08007	https://www.ferreteriabolibar.com/	12
2421	Sabater	physical	41.5338675	2.4204035	Avinguda del Molí de les Mateves, 2, 08310, Argentona	https://sabatergrup.com/	12
2422	Ferreteria A. Ruiz	physical	41.3500966	2.1128696	\N	\N	12
2423	BigMat Silviu	physical	40.4653963	-3.4441429	Avenida de la Constitución, 203	https://www.bigmat.es/es/s/almacenes-de-construccion/madrid/bigmat-silviu-6299	12
2424	Ferreteria Sant Pau	physical	41.6022958	2.6248209	Pujada de Sant Pau, 5, 08395, Sant Pol de Mar	\N	12
2425	Moherclima	physical	41.3881526	2.1376802	310, 08029	https://moherclima.com/	12
2426	Boceguillas	physical	41.334817	-3.6379328	\N	\N	12
2427	Brico Reyes	physical	37.1628483	-5.935695	\N	\N	12
2428	FerreterÍa ROIG	physical	41.3593384	1.9809743	\N	\N	12
2429	Ferretería Irigaray	physical	42.7749115	-1.635927	Calle N, 1-3	https://ferreteriairigaray.com	12
2430	Unfema	physical	43.1850474	-2.4690509	Bidebarrieta kalea, 16	\N	12
2431	Ferretería Marquez Ortega	physical	36.9346212	-3.3268524	\N	\N	12
2432	Aremacotrans S.L.	physical	36.9336822	-3.3298833	\N	\N	12
2433	Obramat_3	physical	41.6148864	0.6569182	Carrer d'Ivars d'Urgell, 25190, Lleida	https://www.bricomart.es/nuestros-almacenes/bm-lleida.html	12
2398	BucofiGrup - portes de seguretat - bústies - caixes fortes - panys	physical	41.3822751	2.134393	08014	http://www.bucofigrup.com	12
2399	JAYPE	physical	39.8869942	4.243606	Avinguda des Cap de Cavalleria, 24, 07714, Maó	https://www.jaype.com/es/inicio	12
2400	Ortez	physical	40.6276501	-4.0079756	\N	\N	12
2401	Novahome	physical	41.4048125	2.1358726	\N	\N	12
2402	Santa Rosa	physical	37.8980052	-4.7795962	La Higuera	\N	12
2403	Onak	physical	43.1852381	-2.4659738	Urtzaile kalea, 2	\N	12
2404	Álvaro Fernández Sánchez	physical	40.3789951	-3.7795567	\N	\N	12
2405	Comerco Cash & Carry	physical	42.168253	0.8870096	Carrer de les Cabanes, 2, 25620, Tremp	\N	12
2406	Comercial BASTOS	physical	42.1497767	-8.6223123	\N	\N	12
2407	Azulejos Porcar	physical	41.3698975	2.1365417	Carrer de la Constitució, 40, 08014, Barcelona	\N	12
2408	Ferrokey_4	physical	40.4586859	-3.7833706	Plaza del Marqués de Camarines	\N	12
2409	Tapias	physical	37.3960066	-1.9391626	\N	\N	12
2444	Ferretería Salamanca	physical	28.4687639	-16.2635408	\N	\N	12
2445	Bricotec	physical	41.1532931	1.1099919	\N	\N	12
2446	Higinio Tabares e Hijos Adeje	physical	28.125349	-16.7434193	\N	\N	12
2447	Ferretería Bravo	physical	40.6591636	-3.7687431	\N	\N	12
2448	Eli	physical	39.5812672	2.6557178	Plaça Alexander Fleming	\N	12
2449	Hezetasuna Burdindegi	physical	43.3495288	-3.0046538	\N	\N	12
2450	Ferreteria Puig_1	physical	42.1826555	2.4903807	\N	\N	12
2451	Ferretería Ezpeleta	physical	42.8546893	-2.678766	\N	\N	12
2452	Valvuleria del Norte	physical	42.8591345	-2.6576913	Eibar kalea, 6, Vitoria-Gasteiz	https://valvuleriadelnorte.es	12
2453	Ferretería Alegria	physical	42.852071	-2.6774171	Domingo Beltran de Otazu kalea, 25 B, 01012, Vitoria-Gasteiz	https://ferreteria-alegria.negocio.site	12
2454	Ferretería Colón	physical	37.2296392	-3.6529436	\N	\N	12
2455	El Tornillo	physical	37.2313735	-3.6515456	\N	\N	12
2456	Ferreteria La Clau_1	physical	39.0778663	-0.5112467	\N	\N	12
2457	Ferretería Marí Luz	physical	39.4406755	-1.9560243	\N	\N	12
2458	Ferretería Elías	physical	38.6641105	-6.1034617	\N	\N	12
2459	Gamma Azagra	physical	41.4680085	-2.5326108	Calle Fresno, 27, 42200, Almazán	http://www.gammaazagra.com	12
2460	Ferretería El Viejo Almacén - Cadena88	physical	43.3716012	-5.8540077	Calle Torrecerredo, 41, 33012, Oviedo / Uviéu	\N	12
2461	DYMA	physical	41.1204752	1.2157557	\N	\N	12
2462	Ferretería Bami	physical	37.3606122	-5.9779004	\N	\N	12
2463	Ferretería Coloma	physical	38.8355629	0.1070575	\N	\N	12
2464	BriCor_5	physical	43.3664082	-5.8495033	Calle General Elorza, 75, 33002, Oviedo / Uviéu	\N	12
2465	Ferretería Luismi	physical	41.5013478	-5.0005132	\N	\N	12
2466	Leroy Merlin_26	physical	41.2272629	1.7406955	Ronda d'Europa, 46	\N	12
2467	Leroy Merlin_27	physical	41.2272266	1.7407143	Ronda d'Europa, 46	\N	12
2468	Ferretería Campoamor	physical	43.3654917	-5.8511532	Calle Campoamor, 10, 33001, Oviedo	\N	12
2469	Brico Garden	physical	40.1095631	-5.777607	\N	\N	12
2470	C.R. Mora	physical	37.2832574	-5.9238143	Calle Melliza, 2, 41701	\N	12
2471	Ferreteria Armengol & Vilumara	physical	41.388601	2.1769451	\N	\N	12
2472	Ferreteria Llanza	physical	41.3971171	2.1721347	\N	\N	12
2473	Ferretería Prieto	physical	43.681721	-7.8532103	\N	\N	12
2474	Ferretería Ruiz_1	physical	36.7040591	-3.4886375	\N	https://www.ferreteriaruiz.com/	12
2475	Torres y Saez	physical	43.0418616	-7.5518279	Rúa Fontán Rodríguez Domingo (físico), 27003, Lugo	\N	12
2476	Mx Subministres, SL	physical	41.2254419	1.7160425	Carrer de Josep Coroleu, 8	\N	12
2477	El Punt del Bon Preu	physical	41.6038189	0.6446194	Carrer de Casimir Vila, 8, 25001, Lleida	\N	12
2478	Josmar	physical	37.3907752	-5.9693716	Calle Sinaí, 38, 41007, Sevilla	\N	12
2479	Ferretería del Puente	physical	40.7528683	-3.786749	\N	\N	12
2480	ISI	physical	42.3438582	-3.690095	Paseo Regino Sainz de la Maza	\N	12
2481	Agrofer	physical	42.8925408	-8.5324295	\N	\N	12
2482	El Martillo_2	physical	38.0937643	-1.7836981	Ronda Este, 30430, Cehegín	\N	12
2483	Beitia cerrajeria	physical	43.1324895	-2.0801611	Iurre auzoa, 14	\N	12
2484	Electroborreguero	physical	37.2811134	-5.925992	Calle Amancio Renes	\N	12
2485	Can Bou	physical	39.7057754	2.7899428	\N	\N	12
2486	Cofedisa	physical	41.1860723	1.5120827	\N	\N	12
2487	MR.D.I.Y.	physical	39.9628845	-4.8297412	\N	\N	12
2488	La Floresta	physical	39.9581952	-4.8468929	\N	\N	12
2489	Tesla	physical	40.4409388	-3.6726418	Calle Clara del Rey, 17, 28002, Madrid	https://ferreteriatesla.negocio.site/	12
2490	Brico Centro_1	physical	40.410216	0.3969713	\N	\N	12
2491	Grupojofer	physical	37.2129162	-7.4097539	\N	\N	12
2492	Brico Dépôt_2	physical	41.6271697	0.6096574	Avinguda de l'Alcalde Rovira Roure, 108,110, 25198, Lleida	http://www.bricodepot.es/	12
2493	La Magdalena	physical	43.5552835	-5.9297777	Calle Doctor Severo Ochoa, 21	\N	12
2494	Ferretería Llaves Santa Clotilde	physical	37.1789831	-3.6120631	Calle Almenillas, 16, 18003, Granada	\N	12
2495	Ganiveteria Marta	physical	41.5203196	0.869818	Raval del Carme, 4, 25400, les Borges Blanques	\N	12
2496	ClickFer Recaval	physical	42.4195076	-6.990556	\N	\N	12
2497	ferrCASH_1	physical	40.363985	-3.5970788	\N	\N	12
2498	Domasa	physical	37.2815542	-5.936771	\N	\N	12
2499	Loysan	physical	42.3587428	-5.3292535	\N	\N	12
2500	Ferretería Bazar_1	physical	42.8798507	-8.5334477	Costa do Vedor, Santiago de Compostela	\N	12
2501	Ferreteria Verlin	physical	41.7887494	0.8089731	Carrer del Molí del Comte, 11, 25600, Balaguer	https://ferreteria-verlin.negocio.site/	12
2502	Ferreteria Pereda	physical	41.9205539	-4.4960771	Calle Primero de Junio, Venta de Baños	\N	12
2504	FV Ferretería	physical	36.9365521	-2.1375039	\N	\N	12
2506	Oria	physical	43.3150178	-1.9812227	Urbieta kalea, 45	https://menajeoria.com	12
2507	Ferretería Yelamo	physical	37.1588762	-3.5911919	\N	\N	12
2508	Brico Rocafort	physical	39.5285396	-0.4115427	\N	\N	12
2509	Cadena 88 - SEF	physical	41.4828812	2.3177834	Carrer d'Itàlia, 18, 08320, El Masnou	https://www.cadena88.com/	12
2510	Bolufer	physical	38.8453462	-0.1152401	\N	\N	12
2511	Drogueria Frigola SL	physical	41.8260491	2.8941734	Carrer d'Àngel Guimerà, 27, 17240, Llagostera	\N	12
2512	J. M. Rodríguez	physical	40.8592165	-3.6128313	\N	\N	12
2516	Ferretería Ramos	physical	36.9374174	-2.1317848	\N	\N	12
2517	Ferreteria_9	physical	41.3540676	2.1132732	Avinguda d'Europa, 95, 08907, L'Hospitalet de Llobregat	\N	12
2869	Calygas	physical	42.1923531	2.5053109	\N	\N	12
2435	Ferretería Marcos	physical	43.4473686	-7.8538833	Avenida de Galicia, 41, 15320	\N	12
2436	Ferreteria Sant Pau_1	physical	41.6021548	2.6246716	\N	\N	12
2437	Ferrokey El Cañaveral	physical	40.4063702	-3.5618228	Avenida Miguel Delibes, 25, 28052, Madrid	\N	12
2438	Qblau instal·lacions hidràuliques	physical	41.1449706	1.105721	\N	\N	12
2439	Bombes Reus	physical	41.145172	1.1065902	Carrer de Miami, 26, 43205, Reus	\N	12
2440	Ferreteria Alco	physical	37.3469613	-5.9790701	\N	\N	12
2441	Car	physical	43.3092843	-1.9678442	Madalena Jauregiberri pasealekua, 4	\N	12
2442	Can Manxa_1	physical	42.1812984	2.4877983	\N	\N	12
2443	Ferreteria Sobrino	physical	42.5998442	-8.7544902	Rúa do Porto, 16-18, 36613	\N	12
2503	Delta Sur S.L.	physical	37.2776343	-5.9321905	\N	https://www.deltasur.es/	12
2505	Ferreteria Casals	physical	41.824671	2.892945	Passeig de Pompeu Fabra, 17240, Llagostera	\N	12
2513	Cadena 88_5	physical	37.9912631	-1.1253222	\N	\N	12
2514	Mobles a mida	physical	41.3857389	2.1490782	Carrer de Viladomat, 227	http://www.moblesamidamd.com	12
2515	KOTHERM	physical	40.476631	-3.642187	Calle de Santa Virgilia, 14, 28033, Madrid	\N	12
2521	Maderas Mariño	physical	42.4938357	-8.8694835	Rúa de Alexandre Bóveda, 55, 36980, O Grove	\N	12
2522	Castells Vilaseca	physical	41.3696085	2.1425289	\N	\N	12
2523	Hijos de Castro Uría	physical	42.5510601	-6.5993333	\N	\N	12
2524	Artieda	physical	41.6597144	-0.8769562	\N	\N	12
2525	Leroy Merlin_28	physical	37.8224765	-0.8088524	\N	\N	12
2526	Bricolage y Ferretería Castillo	physical	37.3444468	-6.0654465	\N	\N	12
2527	Americana	physical	42.3562396	-7.8655209	\N	\N	12
2528	Galinova 2.0	physical	42.3561145	-7.8654967	\N	\N	12
2529	Roma_1	physical	38.9187749	-6.3437068	\N	\N	12
2530	Ferretería Refondo	physical	40.6028422	-4.3348414	\N	\N	12
2531	Salgado	physical	42.3484358	-7.8699804	\N	\N	12
2532	Ibaiondo	physical	43.1746404	-2.4133687	Kalebarren kalea, 14, 20590, Soraluze - Placencia de Las Armas	\N	12
2533	Ferretería Tarazona	physical	39.2597646	-1.9121689	\N	\N	12
2534	Soto_1	physical	41.3762947	2.1212037	\N	\N	12
2535	Ferreteria Jordi	physical	41.4943119	2.2948576	Torrent Vallbona, 5	https://www.cadena88.com/ferrejordi	12
2536	Ferretería Irisarri - Protección Laboral	physical	40.3892341	-3.7298035	\N	\N	12
2537	Ferretería Selen	physical	38.048978	-1.665365	Avenida de Don Luis de los Reyes, 27, 30180, Bullas	\N	12
2538	Ferretería San Fernando	physical	42.6138133	-6.4182749	Calle Maestra Susana González, 11, 24300, Bembibre	\N	12
2539	Ferretería El Remache	physical	36.5900871	-4.5339133	Avenida de las Palmeras	\N	12
2540	Ferretería Benalúa	physical	37.3514585	-3.1677866	\N	\N	12
2541	FerrOkey Galiano	physical	38.5368684	-0.8192088	\N	\N	12
2542	Hdzez de Leon	physical	28.6425509	-17.7752297	\N	\N	12
2560	Bricolaje Juárez S.L	physical	37.9859472	-0.678232	Avenida de las Cortes Valencianas, 12, 03183, Torrevieja	\N	12
2561	Brico Moreno	physical	39.5453141	-0.5733749	Carretera de Vilamarxant, 84, 46190, Riba-roja de Túria	https://www.bricomoreno.es/	12
2562	SEGURCLAU	physical	41.4103739	2.178058	Carrer de Còrsega, 634	https://www.segurclau.com/	12
2563	Terres i Parets	physical	41.73073	1.8348589	\N	\N	12
2564	Ferreteria Teixidor	physical	41.7299988	1.8295067	\N	\N	12
2565	Ferreteria Viola	physical	41.7946331	0.8124859	Carrer de Cervantes, 47, 25600, Balaguer	\N	12
2566	FERRETERIA SALVIA, S.L.	physical	39.961823	-0.263565	Plaza Raval de Sant Josep, 11	https://www.ferreteriasalvia.com/	12
2567	Ferreteria Elviria	physical	36.4956911	-4.7757459	\N	\N	12
2568	Suministros Industriales_1	physical	40.5418143	-3.6263094	\N	\N	12
2593	Ferreteria y Menaje La Torre	physical	41.1447324	1.4040876	\N	\N	12
2594	Ferreteria Bailen	physical	41.2242184	1.714755	Carrer de Bailén, 12, 08800	\N	12
2595	Sia Biosca, S.L.	physical	41.2305345	1.7369288	Ronda Europa, 69, 08800	\N	12
2596	Mx Subministres SL	physical	41.2255136	1.7158815	Carrer Josep Coroleu, 8, 08800	\N	12
2597	Diceltro - Subministraments i ferreteria Industrial	physical	41.2313515	1.7358613	Ronda Ibèrica, 19, 08800	\N	12
2598	Ferreterías Ser-Bric	physical	41.1445141	1.4037069	\N	\N	12
2599	Ferrva	physical	42.8892014	-8.5470688	\N	\N	12
2600	Ferretería Cerrajería Gesco Integral	physical	37.2476571	-1.8705424	\N	\N	12
2601	Ferreteria La Casa de la Herramienta	physical	36.6835111	-6.111156	\N	\N	12
2602	Ferreteria Olivella	physical	41.2209426	1.7224892	Avinguda de Cubelles, 24, 08800	https://www.ferreteriaolivella.com/es/	12
2603	Ferretería Fernández_2	physical	36.5312611	-6.1885225	\N	\N	12
2604	Ferreteria Pallerola	physical	41.2239987	1.7313887	Avinguda del Garraf, 59, 08800	\N	12
2605	Electrònica Joan	physical	41.2256278	1.719106	Carrer del Pare Garí, 19, 08800	https://electronicajoan.com/tienda	12
2606	Central del Bricolatge	physical	41.9721709	2.8217262	\N	\N	12
2607	Ferreteria Daumar	physical	41.2257433	1.722935	Carrer de l'Aigua, 16, 08800	\N	12
2608	Casa Roset	physical	41.2232969	1.7211897	Carrer del Recreo, 65, 08800	https://www.casaroset.com/	12
2609	Valleinclán	physical	28.4594871	-16.2655056	\N	\N	12
2610	Optimus_6	physical	28.4693161	-16.2597351	\N	\N	12
2611	Plus decor optimus	physical	28.4693266	-16.2597141	\N	\N	12
2612	Ferreteria Hijano	physical	41.3719903	2.1211258	Carrer del Progrés, 88, l'Hospitalet de Llobregat	\N	12
2613	Cash brico	physical	28.4586491	-16.2645911	\N	\N	12
2614	Ferretería Ramón Portus	physical	38.1935428	-0.561188	\N	\N	12
2615	Casa Paz	physical	42.782497	-8.6503455	\N	\N	12
2616	Ferreteria Canal	physical	41.6090098	2.2885787	\N	\N	12
2617	Llopis	physical	38.6296313	-0.6701571	\N	\N	12
2618	Son garrit	physical	39.5857795	2.6191037	\N	\N	12
2619	Ferretodo	physical	28.4371079	-16.3190314	Avenida Los Majuelos, Santa Cruz de Tenerife	\N	12
2620	Blasa Sánchez e Hijos	physical	40.3778699	-3.7689727	\N	\N	12
2621	Ferretería Agüero	physical	42.8257378	-1.6167338	\N	\N	12
2622	Krane sistemas	physical	43.4243035	-5.8322814	\N	\N	12
2623	Enriel	physical	43.4238211	-5.8329813	\N	\N	12
2624	Obramat_4	physical	41.1148522	1.225987	Carretera Vella de Valencia, 6 A, Polígon industrial Francoli, 43006, Tarragona	https://www.bricomart.es/nuestros-almacenes/bm-tarragona.html	12
2625	Soto_2	physical	40.752994	-3.784525	\N	\N	12
2626	F. Gilberto	physical	40.8600144	-4.5620522	\N	\N	12
2627	Sufega	physical	37.8782721	-4.7951137	Avenida Guerrita, 9, 14005, Córdoba	\N	12
2628	Ferretería García Hermoso	physical	36.345322	-5.8166622	\N	\N	12
2518	Ferreteria Marina_1	physical	41.3532621	2.1135321	Avinguda d'Europa, 23, 08907, L'Hospitalet de Llobregat	\N	12
2519	Ferreteria JR	physical	27.7696417	-15.5860077	\N	\N	12
2520	Ferreteria_10	physical	27.772268	-15.6057207	\N	\N	12
2543	Lorenzo Rodriguez	physical	28.6503221	-17.8810185	\N	\N	12
2544	Ferrobox_2	physical	28.6566245	-17.908481	\N	\N	12
2545	Brico León	physical	42.5913612	-5.5629958	\N	\N	12
2546	Ferretería Sant Antoni	physical	41.3797786	2.1634436	\N	\N	12
2547	Fergrés	physical	28.04699	-16.6785827	Ctra. General, 65, 38632, Guaza	\N	12
2548	Justijua	physical	40.1892465	-6.1906324	\N	\N	12
2549	Ferretería Ahigaleña	physical	40.1905089	-6.1887106	\N	\N	12
2550	Viuda de Clemente González	physical	39.9631819	-4.8331288	\N	\N	12
2551	Gaspar	physical	28.1821211	-17.2665022	\N	\N	12
2552	Ferretería Casado_1	physical	43.4532383	-3.7431262	\N	\N	12
2553	Ferretería La Curva	physical	36.7584726	-2.9781734	Calle Carretera la Curva, 30, 04770, La Curva	\N	12
2554	J. Miramontes	physical	43.274606	-8.2132989	\N	\N	12
2555	Ferretería Castillo	physical	40.5500587	-3.6541651	\N	\N	12
2556	Ferretería Titanlux	physical	28.4662764	-16.2704443	17	\N	12
2557	Cuchillería Brasil	physical	37.9761228	-0.6792641	Rambla Juan Mateo García, 4, 03181, Torrevieja	\N	12
2558	Elias	physical	41.41048	2.173588	Carrer de Sant Antoni Maria Claret, 202	\N	12
2559	Cadena 88 - Pinturas Imcasa	physical	40.455311	-3.4856122	Avenida de la Constitución, 7	http://www.decoracionesimcasa.com	12
2569	Gérico	physical	41.0635527	-4.7197089	\N	\N	12
2570	BigMat Femalsa	physical	41.0545582	-4.711025	\N	\N	12
2571	BigMat Femalsa_1	physical	41.0543349	-4.7106683	\N	\N	12
2572	Ferreteria Mencey	physical	28.0707887	-16.5565101	Calle Cuevas de Cho Portada, 8, 38611	\N	12
2573	Tolosa	physical	43.1355618	-2.0748491	Lopez-Mendizabal pasealekua, 2	\N	12
2574	Centro_1	physical	42.518237	-0.3649043	\N	\N	12
2575	Ferreteria-Bazar Mila	physical	42.8407344	-2.6954753	\N	\N	12
2576	Ferretería La Muralla	physical	40.3386707	-3.8357684	\N	\N	12
2577	Ferreteria Gaudí	physical	41.4103466	2.1741774	Avinguda de Gaudí, 79	http://www.fdferreterias.com	12
2578	Marín	physical	37.3854602	-5.9489574	Calle General Ollero, 11, 41006, Sevilla	\N	12
2579	F. Urieta	physical	43.2602707	-2.9393449	Alameda San Mamés / Santimami zumarkalea, 42, Bilbao	\N	12
2580	FerrerMadera	physical	36.8899345	-4.1460638	\N	\N	12
2581	Electricidad Lakor	physical	43.3252612	-2.9881021	\N	\N	12
2582	BigMat_6	physical	36.3692404	-5.2304875	\N	\N	12
2583	Comercial Anfeso	physical	40.4001444	-3.6724008	\N	\N	12
2584	Ferretería El Vellón	physical	40.7658967	-3.5830356	Plaza Mayor, El Vellón	\N	12
2585	Ferreteria Optimus_1	physical	41.4148718	2.1649787	Avinguda de la Mare de Déu de Montserrat, 73, 08024, Barcelona	\N	12
2586	El Pilar	physical	40.9731806	-5.66359	\N	\N	12
2587	Ferretería Manzorro	physical	36.2526474	-5.9688157	\N	\N	12
2588	Ferretería Tarantino	physical	41.5639648	2.0067273	\N	\N	12
2589	Innova	physical	41.4097104	2.1766502	Carrer de Còrsega, 631 - 633	https://www.innovareformes.es/	12
2590	Stif Ibérica	physical	41.2214038	1.7113369	Carrer del Doctor Zamenhof, 22, 08800	\N	12
2591	Ferreteria Almirall	physical	41.2217365	1.7186683	Avinguda de Francesc Macià, 105-107, 08800, Vilanova i la Geltrú	https://www.cadena88.com/es	12
2592	Neo Key	physical	41.2223861	1.7188782	Carrer Josep Coroleu, 74, 08800	\N	12
2631	FerreHome	physical	28.3620886	-16.3657932	\N	\N	12
2632	Ferreterías La Herradura	physical	28.3585474	-16.3687956	\N	\N	12
2633	Ferretería Cabrales_1	physical	36.3459839	-5.8160551	\N	\N	12
2634	Ferreteria BAZ Distribuciones	physical	43.2462996	-5.5614828	\N	https://www.grupobaz.es/	12
2656	Ferrihogar	physical	41.1407045	1.1146369	Carrer d'Astorga, 24, Reus	\N	12
2657	Don Bombilla	physical	40.4269681	-3.6857579	\N	\N	12
2658	Ferretería Berriainz	physical	42.831128	-1.593392	\N	\N	12
2659	Ferretería Toraño	physical	43.349884	-5.3286489	Polígono industrial Lleu, Nave 5, 33583	\N	12
2660	Ferreteria Navarro	physical	36.7151775	-4.2809741	\N	\N	12
2661	Ferretería Gutierrez S.L.	physical	28.4783275	-16.4058682	Carretera General del Norte, 174	\N	12
2662	Avellano	physical	43.2722459	-6.6094885	\N	\N	12
2663	Ferreteria Lozano	physical	40.4347847	-3.6441529	\N	\N	12
2664	La Ferretería_5	physical	40.0600146	-5.7536819	\N	\N	12
2665	Ferreteria Jaros SLL	physical	40.3743915	-3.758384	\N	\N	12
2666	Ferretería Los Pedros	physical	42.9966185	-4.1303312	Calle Embutición, 39200, Reinosa	\N	12
2667	Ferretería Riad	physical	41.4023504	2.1593532	Travessera de Gràcia, 187, 08012, Barcelona	\N	12
2674	Ferretería Otero	physical	42.4293519	-8.0787369	\N	\N	12
2675	Ferreteria Venezia	physical	40.6110666	-3.7117157	Avenida de Colmenar Viejo, 5, 28760, Tres Cantos	https://trescantosonline.com/comercios/ferreteria-venecia/	12
2676	Casa Gusmao	physical	40.3911021	-3.7154419	\N	\N	12
2677	Igeldo	physical	43.3281614	-3.0078766	\N	\N	12
2678	Hardware - Eisen Waren	physical	36.7633508	-2.6118614	Avenida de Roquetas de Mar, 99, 04740, Roquetas de Mar	\N	12
2679	FT Maspalomas	physical	27.7667695	-15.5802958	\N	\N	12
2680	Repor 2000	physical	37.2915129	-5.4966163	\N	\N	12
2681	Agro Cuevas	physical	37.2884555	-5.5038729	\N	\N	12
2682	Los Molinos	physical	37.2882388	-5.4947002	\N	\N	12
2683	Ferrtería Industrial Catral	physical	38.1566693	-0.8092454	Avenida de Callosa de Segura, 03158, Catral	\N	12
2684	Ferretería El Juncal	physical	37.3745571	-5.9673527	\N	\N	12
2685	Ferreteria Llull	physical	41.4009599	2.2023156	\N	\N	12
2686	Ferreteria Montoro	physical	39.4977423	-0.3944162	Avinguda de Sant Josep Artesà, 3	\N	12
2687	Ferretería Fortunez	physical	43.4875169	-8.2361053	\N	\N	12
2688	Ferreteria N4	physical	28.9593015	-13.5525931	\N	\N	12
2689	Isaac Gutiérrez	physical	43.3854899	-4.2910498	Plaza de Corro Campíos, 2, 39520, Comillas	\N	12
2690	Garriga	physical	41.2137683	1.1414704	Carrer de l'Horta, 21, la Selva del Camp	\N	12
2691	Ferretería Berlín	physical	41.3838084	2.1397465	Berlín, 69, 08029, Barcelona	\N	12
2692	Ontinyent Ferreteria	physical	38.8230904	-0.6000651	\N	\N	12
2693	Ferretería Hortaleza	physical	40.4734634	-3.6435846	Calle del Mar Caspio, 39, 28033, Madrid	\N	12
2694	Albaladejo	physical	37.805179	-0.837071	\N	\N	12
2695	Ferretería Nalón	physical	43.5605164	-6.0742674	Calle Los Viñales, 33125, L'Arena	\N	12
2696	Ferretería Sa Ronda	physical	39.5112384	3.0269231	\N	\N	12
2629	Ferretería els Martells	physical	41.4008453	2.1581653	Carrer del Penedès, 8-6	\N	12
2630	Suministros Revuelta_1	physical	43.3938152	-3.4612395	\N	\N	12
2635	Ferretería Los Mellizos	physical	40.5843687	-4.1287481	\N	\N	12
2636	Plumed	physical	40.8428701	-1.8843174	\N	\N	12
2637	Aluminios Benalup	physical	36.3504115	-5.8119617	\N	\N	12
2638	Efectos Navales Bada	physical	43.3832441	-4.3988055	\N	\N	12
2639	Marlo_1	physical	28.3567746	-16.3699903	\N	\N	12
2640	Ferresur	physical	36.7199064	-4.6189372	\N	\N	12
2641	Todo En1	physical	40.4393053	-3.645685	\N	\N	12
2642	Guadalix	physical	40.7844985	-3.6998126	\N	\N	12
2643	Spiche	physical	37.1964748	-7.3250839	\N	\N	12
2644	Ferretería Can Carnó	physical	41.7819701	3.0298338	\N	\N	12
2645	Mr. DIY	physical	42.8127287	-1.6371624	\N	\N	12
2646	Ferreteria Deco	physical	41.4472667	1.9759823	Carretera de Barcelona, 103, 08740, Sant Andreu de la Barca	\N	12
2647	BigMat_7	physical	43.2839297	-4.0753863	\N	\N	12
2648	BigMat_8	physical	42.561013	-0.5709669	\N	\N	12
2649	Gripple	physical	41.6795911	-0.9575138	Calle Zuera, 23	\N	12
2650	Araelec	physical	41.6794869	-0.9576103	Calle Zuera, 23	\N	12
2651	Copes. Aluminio y Cerrajería.	physical	41.6785514	-0.9585893	Calle Zuera, 17	\N	12
2652	Fontasa_1	physical	41.6782789	-0.9585008	Calle Zuera, 10	\N	12
2653	Bricocentro	physical	42.2969185	-8.7831782	\N	\N	12
2654	Baños Costa Tropical	physical	36.7413659	-3.5247309	Avenida Doctor Norman Bethune	https://xn--baoscostatropical-gxb.com/	12
2655	Muelles Leyva	physical	40.3935119	-3.71524	\N	http://www.muellesleyva.com	12
2668	Sirvent	physical	41.6125019	2.2899619	\N	\N	12
2669	Ferretería Arenal_3	physical	39.3897141	-3.2108074	\N	\N	12
2670	Ferretería Ruiz_2	physical	38.8901698	-6.6976508	\N	\N	12
2671	Ferretería Industrial Norte	physical	40.4980147	-3.6866085	Calle de Nuestra Señora de Valverde, 130, 28034, Madrid	\N	12
2672	Ferretería García_1	physical	38.8919311	-6.6998056	\N	\N	12
2673	Ferretería Fuencaral Pueblo	physical	40.4936228	-3.6873004	\N	\N	12
2716	Grupo Sanchez Vega Baja S.L	physical	38.0295799	-0.724607	\N	\N	12
2717	Ferretería Fabián	physical	39.4611868	-0.3732374	\N	\N	12
2718	Mercapanys	physical	41.7320461	1.8223199	\N	\N	12
2719	Eurofon	physical	37.9915292	-0.678079	\N	\N	12
2720	Ferretería Vázquez_1	physical	37.5848311	-5.9697207	Calle Vereda de los Rodeos, 51	\N	12
2721	Dragón	physical	37.2466621	-1.8653985	\N	\N	12
2722	FerroPravia	physical	43.4923286	-6.1173995	\N	https://www.ferropravia.es/	12
2723	La ferreteria de l'Oscar	physical	41.2099619	1.6742848	\N	\N	12
2724	Manzano	physical	38.7203618	-5.2232147	\N	\N	12
2725	Ferretería Vista-Alegre	physical	37.9926652	-1.1284666	\N	\N	12
2726	Ferretería Moyano	physical	38.7221003	-5.2224049	\N	\N	12
2754	Kiñu Tools	physical	43.2086965	-2.4218838	\N	\N	12
2755	Ferretería Mercavel	physical	40.3989112	-3.6681343	Avenida de Peña Prieta, 8, 28038, Madrid	\N	12
2756	Ferretería Mos	physical	42.2058552	-8.6570521	Rúa Ludeiro, 31, 36416, Mos	\N	12
2757	Jorman	physical	43.3849549	-5.8212599	\N	\N	12
2758	Hidro-Tec 2000	physical	41.5235521	0.3619486	Polígono Industrial La Concepción, 22520, Fraga	\N	12
2759	Suministros Industriales Cap-pont	physical	41.611123	0.6702221	Polígon Industrial Camí dels Frares, Parcela 2, 2, 25190, Lleida	\N	12
2760	Rodamientos y suministros Cappont, S.L.	physical	41.6107191	0.6707374	Polígon Industrial Camí dels Frares, Carrer A, Nave 2, Parcela 12, 12, 25190, Lleida	\N	12
2761	Ferreteria La Industrial de Lleida	physical	41.6150113	0.6746715	Polígon Industrial Camí dels Frares, Carrer B, Parcela 15, nave 6, 6, 25190, Lleida	\N	12
2762	Ferrecal_2	physical	42.8719796	-8.5443324	Avenida de Lugo, 5, 15703, Santiago de Compostela	https://ferrecal.com	12
2763	Ferretería Busto	physical	43.6156246	-5.7953032	\N	\N	12
2764	Gurea	physical	43.0348422	-2.1859688	\N	\N	12
2765	Optimus_9	physical	41.4303874	2.1786185	\N	\N	12
2766	Leroy Merlin_31	physical	40.6592558	-3.7560059	\N	\N	12
2767	Ferretería Rosaje	physical	36.1765405	-5.3487025	Avenida María Guerrero, 152-154, 11300, La Línea de la Concepción	https://ferreteriarosaje.com/	12
2768	Ferretería Bazar Félix	physical	37.1526861	-1.88947	Avenida de Almería, 66, 04639, Turre	\N	12
2769	Ferretería Mena	physical	36.1684929	-5.3492137	Calle Gabriel Miró, 11300, La Línea de la Concepción	\N	12
2770	Vimar	physical	38.6954028	-0.4865415	\N	\N	12
2771	Maquinaria - Ferretería José Sánchez	physical	40.9563068	-4.1074302	\N	\N	12
2772	Saneamientos Fontanería	physical	40.4591011	-3.7109104	\N	\N	12
2783	Ferreteria Santa Anna - Cadena 88	physical	41.6748612	2.7900648	\N	https://cadena88.com	12
2784	Vda de W. Vila	physical	41.3997724	2.163889	Carrer de Còrsega, 396	\N	12
2785	Pelayo	physical	41.4017226	2.1575519	Carrer del Torrent de L'Olla, 89	\N	12
2786	La Esquina	physical	37.8813089	-4.7965048	Avenida Lagartijo, 3, 14005, Córdoba	\N	12
2787	OPTIMUS - Ferretería Jovi	physical	43.3647552	-5.8347492	Calle Tenderina, 46, 33010, Oviedo	https://www.optimusferreteria.com	12
2788	Ferretería Victorino Martín	physical	40.4098581	-3.7062937	\N	\N	12
2789	Ferretería Venecia_3	physical	40.4223	-3.7106539	\N	\N	12
2790	BricoCentro_2	physical	40.9206149	-4.1130448	\N	\N	12
2791	Ferreteria Les Corts	physical	41.3785103	2.1267693	\N	\N	12
2819	Ferreteria Burgos	physical	41.0803667	1.1366219	Via de Roma, 32, Salou	\N	12
2820	Ferretería PAZ	physical	42.4275348	-8.080444	\N	\N	12
2821	Ferretería Botana	physical	42.4349895	-8.0781422	\N	\N	12
2822	Saneamientos Toledo	physical	40.410305	-3.7102419	Calle del Humilladero, 7	\N	12
2823	Jaime Navarro	physical	39.70682	2.7968908	\N	\N	12
2824	Aguilón	physical	40.3955368	-3.6969559	\N	\N	12
2825	Ferreteria Galdeano	physical	43.0545969	-2.179861	Amerika kalea, 2, 20240	\N	12
2826	Suministros Agrobeni S.L.	physical	39.2884944	-0.4208886	Carrer d'Almussafes, 2, 46450, Benifaió	https://agrobeni.es/	12
2827	La California	physical	28.0309535	-15.4176242	Carretera de Jinámar Telde, 8, 35220	\N	12
2828	Vidal bobinatjes de motors i bombes	physical	41.1453347	1.1063252	\N	\N	12
2829	Vidal bobinatjes de motors i bombes_1	physical	41.1456479	1.1065389	Carrer de Benidorm, 30 LOCAL, 43205, Reus	\N	12
2830	Ferreteria_12	physical	28.1537909	-17.1991179	\N	\N	12
2831	Manuel H El Sereno e Hijos SL	physical	37.578345	-5.9725383	Calle Gaudí, 8	https://gruposereno.es	12
2868	Ferreteria Jumilla Solà	physical	41.5183758	1.7073633	Carrer Nou, 75	\N	12
2697	Hepyc	physical	40.3934529	-3.7106739	\N	https://www.hepyc.com/es/	12
2698	Camps	physical	41.4001035	2.1549883	\N	\N	12
2699	Optimus_7	physical	41.4000531	2.1550527	\N	\N	12
2700	Optimus_8	physical	41.401979	2.1532149	\N	\N	12
2701	Husqvarna_1	physical	39.4856106	2.8922516	\N	\N	12
2702	Leroy Merlin_29	physical	43.3641383	-5.8487443	Calle Posada Herrera, Oviedo / Uviéu	\N	12
2703	Grupo Rajufer	physical	37.5788589	-5.9736549	\N	\N	12
2704	Ferretería Casa Vega	physical	43.4884241	-6.111922	\N	\N	12
2705	Santa Lucía	physical	37.3973046	-5.9827079	\N	\N	12
2706	Ferretería Cruz de la Hermita	physical	37.5807008	-5.9668297	Avda Cruz de la Ermita, 46	\N	12
2707	Leroy Merlin_30	physical	37.6376843	-1.6986887	\N	\N	12
2708	Yosmar	physical	41.1159663	1.2433289	Avinguda Ramón i Cajal, 60, Tarragona	\N	12
2709	TABLEPORT SL, FERRETERIA - PUERTAS Y COCINAS	physical	39.0001427	-0.5250904	Camino Estrecho, 11B, 46800, Játiva	\N	12
2710	Ferretería Vázquez	physical	41.3307896	-5.0821218	\N	\N	12
2711	Burgalesa_1	physical	42.34849	-3.6965061	\N	\N	12
2712	Bdb Aisladis	physical	38.7279171	0.0760388	\N	\N	12
2713	Ferretería Cerrajería Bustamante	physical	43.3173187	-3.0235159	Calle Martín Pérez Zaballas, 4, 48920, Portugalete	\N	12
2714	Ferretería Santos	physical	40.6629662	-3.7683965	\N	\N	12
2715	Maderas Ubago	physical	37.1656825	-3.5892834	\N	\N	12
2727	Ferrymas_3	physical	41.6316292	-0.8866408	\N	\N	12
2728	Ferretería Grego	physical	38.3092884	-5.5950291	\N	\N	12
2729	Fabián	physical	36.7460867	-3.5171861	Calle Nueva, 26, 18600, Motril	https://www.ferreteriafabian.com/	12
2730	UCANCA	physical	28.0777337	-16.5619123	\N	\N	12
2731	Ferretería Abril	physical	37.9941679	-1.1279801	\N	\N	12
2732	Suministros Temagres, SL	physical	38.2791226	-5.8318534	\N	\N	12
2733	Ferreteria La Garita	physical	28.0079413	-15.3767568	\N	\N	12
2734	Celu	physical	36.5386416	-6.1757332	\N	\N	12
2735	La Collera	physical	37.1236005	-1.8331257	Paseo del Mediterráneo, 293, 04638, Mojácar Playa	\N	12
2736	Ferretería El Cristo	physical	43.3562854	-5.8582698	\N	\N	12
2737	D.I.Y. La Zenia	physical	37.925074	-0.7300072	\N	\N	12
2738	Ferreteria_11	physical	27.7572189	-15.6814653	Arguineguin	\N	12
2739	Ferreteria Macosur	physical	27.7720166	-15.6033626	\N	\N	12
2740	Ferretería Zamudio	physical	43.2819164	-2.8637339	\N	\N	12
2741	Ferretería González_1	physical	37.1437171	-1.8272849	Paseo del Mediterráneo, 411, 04638, Mojácar Playa	\N	12
2742	Ferretería Vela	physical	41.6583966	-4.718605	\N	\N	12
2743	Casa Forcada	physical	43.535625	-7.0424639	Rúa do Reinante, 35, 27700	\N	12
2744	Ferreteria albir	physical	39.6977419	-0.7106399	\N	\N	12
2745	Cuchillería Fidalgo	physical	40.6554913	-4.6889929	\N	\N	12
2746	Brico Ferretería M.M.	physical	41.1491985	1.109924	Avinguda de Jaume I, 91, Reus	\N	12
2747	Miramobel S.L.	physical	40.8123812	-3.7670033	Calle de la Fuente, 30, 28792, Miraflores de la Sierra	\N	12
2748	Bricolatge	physical	41.3706501	2.1207911	Carrer del Montseny, 97, 08904, L'Hospitalet de Llobregat	\N	12
2749	Jordi Mallarach	physical	42.1900486	2.5026323	\N	\N	12
2750	Ferreteria Local	physical	40.6286205	-3.1618504	\N	\N	12
2751	Ossu	physical	43.3830906	-3.7381675	\N	\N	12
2752	Ferayu	physical	40.6639792	-3.7737772	\N	\N	12
2753	Ferretería Enric Granados	physical	41.4049066	2.1758611	Carrer de Lepant, 279	\N	12
2773	El Metro Ferretería	physical	39.4354	-0.438847	Carrer de Sant Pasqual, 23, 46210, Picanya	\N	12
2774	Ferreterías Moreno	physical	39.4354249	-0.4341358	Carrer del Marqués del Túria, 1, 46210, Picanya	https://ferreteriasmoreno.com/	12
2775	Ferretería Almatriche	physical	28.11133	-15.43421	Calle de Mariucha, 74, 35012, Las Palmas de Gran Canaria	\N	12
2776	Makijardín	physical	40.6657474	-3.7707917	\N	\N	12
2777	Obramat_5	physical	41.3484927	2.1158798	Carrer de les Ciències, 140, 08908, L'Hospitalet de Llobregat	\N	12
2778	Taller de Ferralla Errimar S.L.	physical	43.1194064	-7.0715132	\N	\N	12
2779	Instal·lacions & Reformes	physical	41.4077879	2.1724685	\N	\N	12
2780	Metalium Arroyo	physical	36.6064357	-4.529942	Calle Concordia	\N	12
2781	Ferretería Ruiz Clares	physical	37.6547065	-2.7700061	\N	\N	12
2782	José Pedro	physical	40.5572062	-5.6710731	\N	\N	12
2792	Las Rías	physical	43.2364109	-7.5593393	Avenida da Terra Chá, 51-53, 27377, A Feira do Monte	\N	12
2793	Ferretería Vidal_2	physical	42.2811649	-8.6097508	Rúa José Regojo, 17, 36800, Redondela	https://ferreteriavidal.es	12
2794	Ferretería Guanarteme_1	physical	28.097388	-15.4424267	Luis Saavedra Miranda, 4, 35014, Las Palmas de Gran Canaria	\N	12
2795	Zuhaitz	physical	43.1698183	-2.6157055	\N	\N	12
2796	Casa Marco	physical	40.3409255	-1.1078072	\N	\N	12
2797	Ferretería Marem	physical	36.1637756	-5.3487772	\N	\N	12
2798	Maquinaria David	physical	36.8990823	-3.4227773	\N	\N	12
2799	s'Avinguda	physical	39.5727671	3.2001782	\N	\N	12
2800	Hiper Almagro	physical	38.8826114	-3.7084976	\N	\N	12
2801	Ferreteria Ingear	physical	41.3968623	2.1645138	\N	\N	12
2802	Ferretería La Llave_2	physical	36.7205013	-4.3548885	Calle Almería, 75, 29017	\N	12
2803	Leroy Merlin_32	physical	38.9742257	-3.9167426	\N	\N	12
2804	Ferretería Cohemar	physical	28.4132068	-16.5532487	\N	\N	12
2805	Ferreteria Baires	physical	37.2008531	-1.8192704	Calle Juan Sebastián Elcano, 24, 04621, Vera Playa	\N	12
2806	Sol_1	physical	37.1764614	-3.6076585	Calle Pintor López Mezquita, 9, 18002, Granada	https://www.cerrajeriasol.es	12
2807	Torresol	physical	43.5376409	-5.9064348	\N	\N	12
2808	La Cadena	physical	36.8421167	-2.4618509	\N	\N	12
2809	Siemens Maquinaria, S.A.	physical	28.0994442	-15.4410447	Calle Diego Vega Sarmiento, 50, 35014, Las Palmas de Gran Canaria	\N	12
2810	Ferreteria L'Orri	physical	42.4104548	1.1301694	\N	\N	12
2811	Bazar Ferretería Gómez	physical	43.0149701	-7.5543317	\N	\N	12
2812	Ferraxería Pardo Freire	physical	43.0159044	-7.2450885	\N	\N	12
2813	Mat.de Contruccion Hnos.Rodriguez	physical	40.3173359	-3.8488401	\N	\N	12
2814	Cal Vidrier	physical	41.5310833	1.6860113	\N	\N	12
2815	González_3	physical	40.1241652	-5.7008248	\N	\N	12
2816	El Candao	physical	36.8429815	-2.4622242	\N	\N	12
2817	Ferretería Ferosan	physical	37.8077438	-2.539554	Avenida de Barroeta, 35, 18830, Huéscar	https://www.ferreteriaferosan.com	12
2818	Auto-Frenos	physical	38.8766266	-6.9581517	\N	\N	12
2832	Ferretería Arcón	physical	43.3464047	-3.7456157	\N	\N	12
2833	Cadena 88 Ferretería San Jose	physical	40.2856051	-3.800945	\N	\N	12
2834	Garaiondo-Bastida	physical	43.2067817	-2.4231834	\N	\N	12
2835	Carmelo Iriondo	physical	43.2069564	-2.4232431	\N	\N	12
2836	Ixos	physical	43.2100106	-2.4184977	\N	\N	12
2837	Becerra Montajes Eléctricos	physical	38.6824288	-7.1015894	Plaza de la Filarmónica, 5	\N	12
2838	R. Martí	physical	41.1520401	1.1043858	Carrer del Doctor Gimbernat, 21, Reus	\N	12
2839	TPF Comercial Burgos	physical	42.3505127	-3.65306	Calle la Lora, 8, 09007, Burgos	https://www.tpfcomercial.com/	12
2840	Bopra	physical	38.9092954	1.4287183	\N	\N	12
2841	Comercial Fanum SL	physical	42.4594695	-6.0612881	\N	\N	12
2842	MCC Materiales De Construccion Cristobal Castilla, SL	physical	36.4323768	-5.4491666	Avenida los Deportes, 5	\N	12
2843	Ferretería La Llave_3	physical	36.7210526	-4.4098203	Paseo de Reding, 31, 29016	\N	12
2844	Manitas del Hogar	physical	40.4381261	-3.6498515	\N	\N	12
2845	Droguería Ferretería Antonino	physical	37.1813556	-6.9604243	\N	\N	12
2846	Casa Barranco	physical	37.8700616	-4.1856174	\N	\N	12
2847	Frías	physical	40.3843759	-3.754292	\N	\N	12
2848	FerrOkey	physical	40.462026	-3.4814577	Calle de Madrid, 4	https://www.ferrokey.eu/ferrokey-torrejon-ferreteria-jardin	12
2849	Ferreteria Aguilera	physical	42.7840433	0.6919066	Carrèr dera Aigua, 5, 25550, Bossòst	\N	12
2850	Manso	physical	40.4069347	-3.7081083	Plaza del Campillo del Mundo Nuevo, 1	\N	12
2851	Tambre	physical	42.9091917	-8.7355003	\N	\N	12
2852	CELO Fixings España	physical	41.6043353	2.0908626	Carrer del Rosselló, 7, 08211, Castellar del Vallès	https://www.celofixings.es	12
2853	Melchor	physical	42.7581298	-8.9486751	\N	\N	12
2854	Agrisur Morente Ramírez	physical	37.8710861	-4.1894218	\N	\N	12
2855	Alpe S.L.	physical	42.2318724	-8.4550288	\N	\N	12
2856	FSáenz_1	physical	36.7338477	-4.4169802	Calle Zurbarán, 23	https://www.fsaenz.com/	12
2857	Ferreteria Cuyàs	physical	41.5018783	1.8142682	\N	\N	12
2858	Mengual	physical	41.5940426	2.2799732	Carrer Ronçana, 12, 08400, Granollers	https://www.mengual.com/	12
2859	Ferretería Las Flores	physical	36.7352714	-4.421804	Calle Obispo Bartolomé Espejo, 9, 29014	\N	12
2860	Ferreteria Amorós	physical	41.7094422	0.9027443	Carrer de Pons i Arola, 30, 25240, Linyola	\N	12
2861	El Arroyo	physical	40.2766091	-3.8014622	Plaza de Valdeserrano, 9	\N	12
2862	Ferretería Ros	physical	41.0793609	1.133659	\N	\N	12
2863	Ferretería Arroyo	physical	40.4731682	-3.5789768	\N	\N	12
2864	Ams	physical	43.556364	-5.92966	Calle Doctor Severo Ochoa, 27	\N	12
2865	iReparo	physical	38.9687317	-0.1789592	\N	\N	12
2866	Ferrymas_4	physical	39.2820062	-0.4255495	Avinguda de les Germanies, 27, 46450, Benifaió	\N	12
2867	Valfer	physical	42.1550504	-8.7181229	\N	\N	12
2889	Aluminios CRESMAR S.L.	physical	41.3707896	2.1375728	Carrer d'Olzinelles, 95-97, 08014, Barcelona	\N	12
2937	Cadena 88_6	physical	28.0522197	-16.7151422	\N	\N	12
2938	Jeysa	physical	42.7741038	-7.4137417	\N	\N	12
2939	CASA MARISIN	physical	40.7066973	0.7156193	\N	\N	12
2940	Ferretería Villa de Arico	physical	28.1655834	-16.5017862	Carretera General del Sur, 27, 38580	\N	12
2949	Karim	physical	41.3727645	2.120406	carrer del Progrés, 80, 08904, L'Hospitalet de Llobregat	\N	12
2950	Agricentro Ferretería A.M.Martinez	physical	37.5909425	-5.8733649	\N	\N	12
2951	Ferretería Gómez	physical	37.5898269	-5.8759131	\N	\N	12
2952	Ferretería Adriano	physical	37.5507603	-5.8695503	\N	\N	12
2953	Ferretería Cerrajería Miguel	physical	37.550395	-5.8698797	\N	\N	12
2954	Martí Electrodomèstics	physical	40.7172005	0.7324656	Carrer de la Unió, 40, 43580	https://www.martielectrodomestics.es	12
2955	Ferretería Valdés	physical	36.1365169	-5.8461615	\N	\N	12
2956	Saneamientos Hermanos Díaz	physical	40.3768792	-3.6212407	\N	\N	12
2957	Toledo	physical	40.5546233	-3.3265142	Calle Cristo, 5B, 28880, Meco	\N	12
2958	Lowell	physical	40.4430309	-3.6518218	Calle Aristóteles, 28027, Madrid	\N	12
2959	Ferblanda	physical	41.6764613	2.7896871	\N	https://www.optimusferreteria.com/tienda/ferblanda-94/	12
2960	Ferreteria Jorba	physical	41.8472562	2.3891537	\N	\N	12
2961	Ferretería Carlos Moya	physical	39.1486884	-3.0255115	Paseo San Isidro, 16	\N	12
2962	Castelao	physical	42.6074093	-6.8087543	\N	\N	12
2963	Sandes & Cao	physical	42.6070088	-6.8088683	\N	\N	12
2964	Comercial Artieda	physical	41.634542	-0.8785107	\N	\N	12
2965	Drogueria Elixir	physical	38.3980589	-0.4346553	plaza José Sala Pérez, 03550, San Juan de Alicante	\N	12
2966	Drogueria Royaripi	physical	38.3996942	-0.434004	carrer de l'Ordana, 8, 03550, San Juan de Alicante	https://royairpi.com/	12
2982	Ferreteria Nadal	physical	41.6189014	1.0077843	\N	\N	12
2983	La Ferreteria	physical	41.5476692	0.8253832	Carrer de La Font, 12,14, 25430, Juneda	\N	12
2984	Ferretería Escobar	physical	43.3051435	-5.6905497	Calle Manuel Suárez García, 3, 33930, Langreo / Llangréu	\N	12
2985	Bricogran	physical	36.178129	-5.3780747	Calle Obispo, 3, 11314, Campamento	\N	12
2986	Yarza	physical	43.3097508	-1.9802514	\N	\N	12
2987	Brico Sarria	physical	42.7815444	-7.4142364	\N	\N	12
2988	BdB Amaya Quintero	physical	36.2920292	-6.0950933	Carretera El Pradillo, 11140, Conil de la Frontera	https://www.grupobdb.com/tienda/2585/jose-amaya-quintero-sl	12
2989	Obramat_7	physical	41.2378362	1.7300189	Carrer de l'Acer, 13, 08800, Vilanova i la Geltrú	https://www.obramat.es/nuestros-almacenes/bm-vilanova.html	12
2990	Obramat_8	physical	41.5179043	2.1001599	Carrer de la Serra de Galliners, 24, 08205, Sabadell	\N	12
2991	Ferretería Blister	physical	37.1728104	-3.6061959	\N	\N	12
2992	Ferretería Espelect	physical	37.382016	-6.1232028	\N	\N	12
2993	Aldana_1	physical	43.3067417	-2.3879693	\N	\N	12
2994	EcoPack Biodegradables & Compostables	physical	39.4766836	-0.390039	\N	\N	12
2995	Ladrillos Deltebro	physical	40.7195066	0.7214198	\N	\N	12
2996	Ferreteria industrial - materials de construcció	physical	40.7302308	0.709368	\N	\N	12
2997	BricoCentro_3	physical	39.1727672	-3.0220181	Camino de Alcázar, 36	https://www.bricocentrotomelloso.es/	12
3000	Justo	physical	43.3098011	-3.0094772	\N	\N	12
3001	TOFER A.V.G.	physical	39.1657661	-3.0293212	Carretera de Argamasilla de Alba, km. 1.3, 13700, Tomelloso	https://www.tofer.es/	12
3002	Suministros Urnisa	physical	42.3450402	-3.6876556	\N	\N	12
3003	Romia	physical	43.3534781	-8.2547037	\N	\N	12
3004	Ferreteria Occitana	physical	37.3033952	-3.1358157	\N	\N	12
3005	Ferretería Alcosa Bellido	physical	37.4073235	-5.9237611	Avenida Ildefonso Marañón Lavín, 41019	\N	12
2870	Bricolatge Comas	physical	42.1251664	3.136061	\N	\N	12
2871	Ferreteria Palero	physical	39.2872699	-0.4258203	Carrer de Regino Mas, 3, 46450, Benifaió	\N	12
2872	Gómez Trujillo SC	physical	36.5543001	-4.6141167	Avenida de Los Boliches, 93, 29640, Fuengirola	\N	12
2873	Suministros Aguilera	physical	37.8727466	-4.1756626	\N	\N	12
2874	Ferretería Carnero Luque	physical	36.7397722	-4.4813476	Carril del Molino, 4	\N	12
2875	Adarra Suministros Industriales	physical	43.2647522	-1.9679153	Zikuñaga bailara, 27, 20120, Hernani	\N	12
2876	Iri-be	physical	43.1126088	-2.4138306	\N	\N	12
2877	La Industrial Ferretera	physical	41.5088236	-5.7477264	Calle de Villalpando, 38, 49005, Zamora	\N	12
2878	Veralia	physical	40.4382299	-3.7112685	Calle de Blasco de Garay, 65	\N	12
2879	Danipa Suministro Industrial	physical	40.0220136	-3.8578167	\N	\N	12
2880	Mestral La Ferreteria	physical	41.6748059	2.7903206	\N	https://www.laferreteria.shop/	12
2881	Ferretería Alicantina	physical	38.7422278	-0.4399601	\N	\N	12
2882	Suministros Correa	physical	36.7467649	-3.5125002	Calle Manuel de Falla, 13	\N	12
2883	Ferreteria Ca n'Oriol	physical	41.4963888	2.0397372	Carrer de la Pastora, 13, 08191, Rubí	http://www.ferreteriacanoriol.com/	12
2884	Ferretería y Suministros Industriales Ruma	physical	41.4947554	2.0374522	Carrer de la Mare de Déu de Lourdes, 17, 08191, Rubí	http://www.ferreteriaruma.es/	12
2885	Ferretería Juan	physical	36.7283204	-4.4134773	Calle Compás de la Victoria, 17, 29012	\N	12
2886	SESAtools	physical	43.2710835	-1.9700345	\N	\N	12
2887	Argi ferretería	physical	43.3254004	-2.987312	\N	\N	12
2888	Brico Encartaciones - La cadena 88	physical	43.2008659	-3.0498635	\N	http://www.bricoencartaciones.com/	12
2890	Bazar Donde Yong	physical	40.4372663	-3.6440129	\N	\N	12
2891	Ferreteria Edifesa	physical	41.4063656	2.1700015	\N	\N	12
2892	Ferreteria Tomàs	physical	40.719696	0.7303525	\N	\N	12
2893	Materials Homs	physical	41.4938426	2.3228357	Avinguda de José Roca Suárez-Llanos, 43, 08329, Teià	\N	12
2894	Ferreteria Tarraco	physical	41.1148509	1.246099	Carrer Mallorca, 13, Tarragona	\N	12
2895	Fesmes	physical	41.9706851	2.8378434	Carretera de Sant Feliu de Guixols, 18-20, 17004, Girona	\N	12
2896	Brico Planet	physical	36.7296334	-4.4155479	Calle Manrique, 19, 29013	\N	12
2897	Almacenes Vaz Estévez S.L. (Gamma)	physical	40.2035489	-6.8684105	\N	https://www.vazestevez.com/	12
2898	Almacén Central	physical	42.7811399	-7.4146661	\N	\N	12
2899	Emilio Piñeiro	physical	42.7830085	-7.4174363	\N	\N	12
2900	Professional Pools	physical	37.7969	-0.838193	\N	\N	12
2901	José Domingo ferretería	physical	42.4172728	-2.7318077	\N	\N	12
2902	RAFE	physical	39.7692592	3.0258159	\N	\N	12
2903	Sayez	physical	40.2462099	0.2792511	Calle Blasco Ibáñez, 5, 12579, Alcossebre	https://ferreteriasayez.com/	12
2904	Ortega	physical	43.3058134	-1.9764392	Felipe IV.a hiribidea, 2	\N	12
2905	Ideo Brico	physical	43.4332596	-3.9140915	\N	\N	12
2906	Ferretería J.A. Quintero	physical	40.3670255	-3.5380261	\N	\N	12
2907	Happy Asia	physical	40.440317	-3.6433548	\N	\N	12
2908	Ferreteria Montseny_1	physical	41.294808	1.256116	Carretera del Pla, 100, 43800, Valls	\N	12
2909	Ferretería El Candil	physical	40.3203287	-3.7555191	Calle de Oviedo, 7, 28914, Leganés	\N	12
2910	Ferretería Martínez_1	physical	42.8311758	-1.6362137	\N	\N	12
2911	Ferreteria Hassan	physical	41.2877282	1.2560322	Carrer Vallvera, 2, 43800, Valls	\N	12
2912	Taller Salvat	physical	41.3036692	1.2619176	Carretera del Pla, 172, 43800, Valls	https://www.tallersalvat.com/	12
2913	Ferreteria Martí_1	physical	40.7176649	0.7325691	\N	\N	12
2914	Obramat_6	physical	39.4127447	-0.3882817	\N	https://www.bricomart.es	12
2915	ALTADILL Electrodomèstics	physical	40.8044467	0.5186606	\N	https://www.altadill.com	12
2916	Taller Salvat_1	physical	40.6854586	0.5825034	Carrer del Loira, 36, 43870, Amposta	https://www.tallersalvat.com/	12
2917	Bricolatge i pintures Ricote	physical	41.1150411	1.2484964	Carrer del Cardenal Cervantes, 35, Tarragona	\N	12
2918	Colom	physical	41.850133	2.2281052	\N	\N	12
2919	MON divers - electrodomèstics	physical	40.7197885	0.7252648	Avinguda de la Generalitat, 26, 43580	\N	12
2920	OPTIMUS - FERRETERIA TEKNIK	physical	40.7251052	0.7205819	43580	\N	12
2921	IXOS	physical	40.7215084	0.725345	\N	\N	12
2922	Celeiro	physical	42.766642	-7.567547	\N	\N	12
2923	Rachadell	physical	39.4218934	-0.3889022	\N	\N	12
2924	FT Selección	physical	29.2304991	-13.5031981	\N	\N	12
2925	Ferreteria Cardeñosa	physical	41.4350928	2.2043178	\N	\N	12
2926	Ferraxaría Atán	physical	42.9376128	-8.9918105	\N	\N	12
2927	Optimus Ferretería Teatinos	physical	43.3719432	-5.8367252	\N	\N	12
2928	ALUPRAGAR	physical	40.7104972	0.7180511	Carrer de Sant Joan, 46	\N	12
2929	Würth_8	physical	40.456739	0.4494911	\N	\N	12
2930	Supervía Electricidad	physical	41.6670962	-0.8319041	Avenida de Santa Isabel, 101	\N	12
2931	Ferretería Sola	physical	37.3540618	-2.2965768	\N	\N	12
2932	Ferretería América	physical	37.3833196	-2.1399603	\N	\N	12
2933	Ferretería Lepanto	physical	37.380458	-2.1358327	\N	\N	12
2934	Comercial Marhuenda	physical	37.3554645	-2.2960923	\N	\N	12
2935	Würth_9	physical	38.5323013	-0.1670309	\N	\N	12
2936	J. Bellón	physical	42.8934789	-8.5476569	\N	\N	12
2941	Würth_10	physical	36.7370147	-3.5127286	\N	\N	12
2942	Cruz	physical	42.9274529	-8.4814773	\N	\N	12
2943	Ferrateria Vives	physical	41.2877207	1.2514863	Passeig dels Caputxins, 3, 43800, Valls	\N	12
2944	Ferrateria Serra	physical	41.2860959	1.2503807	Plaça del Pati, 9, 43800, Valls	\N	12
2945	Ferretería Boel	physical	42.8753992	-8.5507315	Avenida de Rosalía de Castro, 36, Santiago de Compostela	\N	12
2946	Llorente	physical	40.7796371	-4.4130336	19, 40150, Villacastín	\N	12
2947	Julio Rico	physical	42.2390091	-8.7265585	\N	\N	12
2948	Pitoina	physical	36.8275751	-4.5362016	Calle Arrabal de los Ángeles, 29150, Almogía	\N	12
2967	Tropical	physical	40.2881857	-3.8043665	\N	\N	12
2968	VIDRE - ALUMINI	physical	40.7505537	0.6270809	\N	\N	12
2969	La Muralla_1	physical	40.3477113	-3.8090861	Avenida de la Libertad, 28924, Alcorcón	\N	12
2970	Factotum	physical	41.3928739	2.1786368	Passeig de Sant Joan, 24, 08010	http://www.factotum168.com	12
2971	Ferretería Torres Vélez	physical	37.492802	-2.7740353	Avenida de Granada	\N	12
2972	Quintana	physical	42.7802547	-7.4104993	\N	\N	12
2973	Ferreteria San Anton	physical	37.3517147	-2.1949625	\N	\N	12
2975	Comercial Arques (magatzem)	physical	40.7035278	0.7151605	\N	https://comercialarques.com/	12
2976	Comercial arques (exposició)	physical	40.7041472	0.716883	Carrer del Cid, 21	https://comercialarques.com/	12
2977	Cadena 88_7	physical	37.3021194	-6.2976591	\N	\N	12
2978	Fecogar	physical	38.4846469	-0.778829	\N	\N	12
2979	Covilma	physical	40.4147729	-4.4984801	\N	https://www.covilma.com/	12
2980	Ferreteros Zamoranos	physical	41.5050352	-5.7519108	Calle de la Puentica, 11, 49031, Zamora	\N	12
2981	Juan Esteban	physical	36.962377	-3.0512517	\N	\N	12
2998	La Ferreteria_1	physical	39.1701294	-3.0213482	Carretera de Argamasilla de Alba	\N	12
2999	La Ferretera Gallega	physical	42.4316618	-8.6345042	\N	\N	12
3080	Ferreteria Sabadell	physical	41.4742187	2.0897608	Passeig de la Torre Blanca, 35, 08172, Sant Cugat del Vallès	https://laferresantcugat.com/	12
3081	Brico Alfer - Ferreteria Alcaraz	physical	42.1135597	3.1421115	\N	\N	12
3082	Ferraxaría Norio	physical	42.2692143	-8.6704337	Avenida de Vigo, 172, 36320, Chapela	\N	12
3083	Bricolaje Cruz	physical	36.1785708	-5.3699397	\N	\N	12
3084	Can Toni Reia	physical	39.7670141	2.7160813	\N	\N	12
3085	La Casa	physical	38.5071277	-5.1470687	Carretera de Belalcázar, 22, 14270, Hinojosa del Duque	\N	12
3086	Ferretería Trujillo	physical	37.0078793	-6.5636522	\N	\N	12
3087	Ferreteria Caja	physical	38.4966519	-5.1389788	Avenida Nuestra Señora del Pilar, 14270, Hinojosa del Duque	\N	12
3127	Leroy Merlin_50	physical	\N	\N	\N	\N	12
3128	GiFi	physical	\N	\N	\N	\N	12
3129	Torsesa	physical	\N	\N	Avenida Montes Sierra, 5	\N	12
3130	Leroy Merlin_51	physical	\N	\N	\N	\N	12
3131	Leroy Merlin_52	physical	\N	\N	Rúa de Polonia, 1, 15707, Santiago de Compostela	\N	12
3132	Leroy Merlin Alcalá de Guadaíra	physical	\N	\N	Calle Fridex Tres, Alcalá de Guadaíra	\N	12
3133	La Unión	physical	\N	\N	\N	\N	12
3134	Brialta	physical	\N	\N	\N	\N	12
3135	Brico Dépôt_4	physical	\N	\N	\N	\N	12
3136	Leroy Merlin_53	physical	\N	\N	Avenida La Ribera, 48903, Barakaldo	\N	12
3137	Bauhaus_6	physical	\N	\N	\N	\N	12
3138	Leroy Merlin_54	physical	\N	\N	\N	\N	12
3139	Leroy Merlin_55	physical	\N	\N	\N	https://www.leroymerlin.es/tiendas/aldaia	12
3140	Leroy Merlin_56	physical	\N	\N	08349, Cabrera de Mar	\N	12
3141	Apalliser	physical	\N	\N	Camí de ses Rodees, 10, 07714	\N	12
3142	Torres & Sáez	physical	\N	\N	Estrada dos Baños de Arteixo, 22, 15008, A Coruña	https://www.torresysaez.com/	12
3143	Leroy Merlin_57	physical	\N	\N	\N	https://www.leroymerlin.es/tiendas/compact-ferrol	12
3144	Brico Dépôt_5	physical	\N	\N	\N	\N	12
3145	Bricoking	physical	\N	\N	\N	\N	12
3146	Leroy Merlin_58	physical	\N	\N	\N	https://www.leroymerlin.es/	12
3147	Ferretería Orfila, S.L.	physical	\N	\N	Carrer de Biniarroca, 35, 07711	\N	12
3148	Directe	physical	\N	\N	Avinguda Circumvalació, 7, 07711	\N	12
3149	Leroy Merlin_59	physical	\N	\N	\N	\N	12
3150	Fes Mes	physical	\N	\N	\N	\N	12
3151	Chafiras	physical	\N	\N	\N	\N	12
3152	Chafiras Adeje	physical	\N	\N	38670	https://chafiras.com/	12
3153	Salvador Escoda	physical	\N	\N	\N	\N	12
3154	Brico Dépôt_6	physical	\N	\N	\N	https://www.bricodepot.es/	12
3155	Leroy Merlin_60	physical	\N	\N	\N	\N	12
3156	Leroy Merlin_61	physical	\N	\N	Carretera Majadahonda a Boadilla, 28222, Majadahonda	https://www.leroymerlin.es/tiendas/majadahonda.html	12
3157	Jomar	physical	\N	\N	Avinguda de la República Catalana, 17487, Empuriabrava	\N	12
3158	Leroy Merlin_62	physical	\N	\N	\N	\N	12
3159	Comercial Alba-Fenar	physical	\N	\N	Calle de la Milana, 2, 24640, La Robla	\N	12
3160	Reloga	physical	\N	\N	\N	\N	12
3161	Tentcosta	physical	\N	\N	\N	\N	12
3166	Coarco	physical	\N	\N	\N	\N	12
3167	Leroy Merlin_64	physical	\N	\N	\N	\N	12
3182	BdB Esteso_1	physical	\N	\N	\N	\N	12
3183	Cementos Mollet	physical	\N	\N	Avinguda de Rafael Casanova, 116	\N	12
3184	Mausa	physical	\N	\N	Carrer de Can Milans, 2, 08110, Montcada i Reixac	\N	12
3185	Ceràmica CABESTANY, S.L.	physical	\N	\N	Camí de les Toeses	\N	12
3186	Everak	physical	\N	\N	\N	\N	12
3187	Leroy Merlin_68	physical	\N	\N	Camino Loma de San Julián	\N	12
3188	Bricor Arroyomolinos-Xanadú	physical	\N	\N	\N	\N	12
3189	BricoTiendas	physical	\N	\N	\N	\N	12
3190	Effectos Navales Hogar Nautica	physical	\N	\N	Calle Gobernador José García Hernández	\N	12
3216	Jardimaq	physical	\N	\N	14, 15917, Padrón	\N	12
3217	Ferreteria_15	physical	\N	\N	22430, Graus	\N	12
3218	Camina	physical	\N	\N	\N	\N	12
3219	MAPRISE	physical	\N	\N	\N	\N	12
3220	Saneamientos Pereda_1	physical	\N	\N	\N	\N	12
3221	Celso Míguez	physical	\N	\N	\N	http://www.celsomiguez.com/	12
3222	Albert Solé	physical	\N	\N	Avinguda de l'Alcalde Porqueres, 111, 25005, Lleida	\N	12
3223	Brico Dépôt_11	physical	\N	\N	Rúa Severo Ochoa, 21, 15008, A Coruña	https://www.bricodepot.es/	12
3224	Leroy Merlin_72	physical	\N	\N	\N	\N	12
3225	Saltoki	physical	\N	\N	Carrer de Salt, 3, 17005, Girona	https://www.saltoki.com/	12
3226	Rodilla - Ferretería Profesional y Bricolaje	physical	\N	\N	Calle Hoces del Duratón, 78, 37008, Salamanca	\N	12
3239	Leroy Merlin_74	physical	\N	\N	\N	\N	12
3240	Ferreteria Los Manantiales_1	physical	\N	\N	\N	\N	12
3241	Cifec	physical	\N	\N	Carrer Espardenyers, 2-3, 43400, Montblanc	\N	12
3242	Es Brico_1	physical	\N	\N	\N	\N	12
3243	Can Mac	physical	\N	\N	\N	\N	12
3244	Manacor	physical	\N	\N	\N	\N	12
3245	Morey	physical	\N	\N	\N	\N	12
3246	Bricolajes Rincón	physical	\N	\N	Calle de la Florida, 18, 28670, Villaviciosa de Odón	\N	12
3247	Brico Dépôt_13	physical	\N	\N	El Pedréu, 33468, Tresona	\N	12
3248	Pedro Villena Romero	physical	\N	\N	\N	\N	12
3249	J. Villaverde	physical	\N	\N	\N	\N	12
3250	Soluciones Integrales de Futuro	physical	\N	\N	\N	\N	12
3251	Almacenes Tocho	physical	\N	\N	\N	\N	12
3252	Pérez Espinosa	physical	\N	\N	\N	\N	12
3253	Sastre Roca	physical	\N	\N	\N	\N	12
3254	Ceferino de la Iglesia - Big Mat	physical	\N	\N	San Marco, Abegodo, 15318, Abegondo	\N	12
3255	Big Mat	physical	\N	\N	\N	\N	12
3256	Brico Dépôt_14	physical	\N	\N	\N	\N	12
3257	Brico Dépôt_15	physical	\N	\N	\N	\N	12
3258	Tucasa	physical	\N	\N	\N	\N	12
3259	Almacenes Femenías	physical	\N	\N	\N	\N	12
3260	Premajor	physical	\N	\N	\N	\N	12
3261	Bauhaus_9	physical	\N	\N	\N	\N	12
3262	Ferretería Tejina	physical	\N	\N	\N	\N	12
3263	Comercial Metabos_2	physical	\N	\N	Avenida de Carbajosa, 7, 37188, Carbajosa de la Sagrada	http://www.metabos.com	12
3264	Can Soler	physical	\N	\N	\N	\N	12
3265	Brico Marian	physical	\N	\N	\N	\N	12
3006	Ferretería Elias	physical	43.020642	-7.5631931	\N	\N	12
3007	Víctor Díaz	physical	39.4531087	-5.3308835	\N	\N	12
3008	Merino_1	physical	40.3544206	-3.6868205	\N	\N	12
3009	Ferretería Suministros Correa	physical	36.7523197	-3.5165872	Calle Ancha, 14, 18600, Motril	\N	12
3010	Comercial Mosabe	physical	36.7469911	-3.5144033	\N	https://www.comercialmosabe.com/	12
3011	Susanfo Suministros Sanitarios y Fontanería	physical	36.6062902	-4.5317027	Calle Moscatel, 29, 29631	\N	12
3012	Colors	physical	42.2656333	3.1757487	Carrer del Doctor Arruga, 14, 17480, Roses	\N	12
3013	Ferreteria Estacion	physical	37.9776862	-0.6919549	\N	\N	12
3014	Ferreteria Torreaguas - Cadena88	physical	37.9835362	-0.6797415	\N	\N	12
3015	Ferretería Vicente	physical	37.2610826	-6.0721887	\N	\N	12
3016	Ferretería Criado	physical	40.6620106	-3.7653006	\N	\N	12
3017	Frior	physical	42.9886528	-8.8749429	\N	https://frior.es/	12
3018	Ferretería Ochoa	physical	37.8720798	-4.793216	\N	\N	12
3019	Suministros Gary	physical	36.6970582	-4.4889841	Calle Leopoldo Lugones, 43, 29004	\N	12
3020	Ferretería Rodríguez	physical	40.6579836	-3.7753392	\N	\N	12
3021	El Sabio	physical	41.6696411	-0.8391983	Avenida de Santa Isabel, 18	\N	12
3022	ferremaclet	physical	39.4862317	-0.362588	\N	\N	12
3023	Rucho_1	physical	42.8548672	-7.1634018	\N	\N	12
3024	Ferreteria Mas Ventura	physical	42.1989958	2.6932533	\N	\N	12
3025	Ferretería Siled	physical	40.3832657	-3.7053775	\N	\N	12
3026	HIPER ASIA	physical	41.6665083	-0.8332342	Calle de la Reina de Portugal, 9	\N	12
3027	INSTAL·LACIONS VICTOR	physical	40.6941736	0.7197091	Avinguda de Mallorca, 59	\N	12
3028	FONTELCO	physical	40.7020884	0.7174425	\N	\N	12
3029	Materials Pardo	physical	41.5169033	1.6244626	\N	\N	12
3030	FERRETERIA SOLUFER	physical	36.7595527	-2.9751753	Calle Minerva, 9, 04770, La Curva	\N	12
3031	La Clau del Pirineu	physical	42.1654782	0.8950337	Avinguda d'Espanya, 8, Tremp	\N	12
3032	Tectime	physical	40.3911881	-3.7279604	\N	\N	12
3033	Comercial Perfilan S.L.	physical	28.9770904	-13.5251636	Carretera los Marmoles, 1, 35550, Arrecife	\N	12
3034	Ferretería Gil	physical	40.3096269	-3.719813	Avenida de los Ángeles, 31, 28903, Getafe	\N	12
3035	Brico Doñana	physical	37.1324288	-6.4891838	\N	\N	12
3036	La Muralla_2	physical	37.8933983	-4.7700907	\N	\N	12
3037	Instaladora Sevillana	physical	40.3975668	-3.768127	\N	\N	12
3038	Ferreteria_13	physical	40.3976736	-3.7701009	\N	\N	12
3039	Jovani	physical	40.3984005	-3.774548	\N	\N	12
3040	Cadena 88_8	physical	40.3984831	-3.7743536	\N	\N	12
3041	Carpintería Kaithermik	physical	43.2958753	-2.2500494	Santiago auzoa, 20, 20750, Zumaia	\N	12
3042	Gómez	physical	40.5507603	-3.322877	\N	\N	12
3043	Papelaría-Ferraxaría O Garabato	physical	42.6561757	-7.3641511	\N	\N	12
3044	Kärcher Center	physical	40.3695204	-3.7444168	\N	\N	12
3045	Ferryhogar	physical	36.7377228	-4.3808014	\N	\N	12
3046	Ferreteria Molinet	physical	41.7871059	1.0919294	Carretera d'Artesa de Segre, 1, 25310, Agramunt	http://www.molinet.cat/	12
3047	Ferretería García_2	physical	42.7855787	-8.8842162	Corredoira de Luís Cadarso Rey	\N	12
3048	Quiros	physical	36.5355804	-6.2992024	\N	\N	12
3049	Manuel Vázquez Pérez	physical	43.4848671	-8.2293679	Rúa Rochel, 30-32	\N	12
3050	Ferretería Tucho	physical	42.7818463	-8.8861501	Avenida do Malecón de San Lázaro	\N	12
3051	Ferretería Gefrán	physical	36.1678522	-5.3461937	Calle Padre Pandelo, 11300, La Línea de la Concepción	\N	12
3052	Leroy Merlin - ENTREGA DE MERCADERIA	physical	41.3288858	2.0479922	\N	\N	12
3053	BdB Ramon Tomàs (Raycor)	physical	41.5614717	0.5153788	avinguda de Catalunya, 227, 25180	\N	12
3054	Ferretería Óptimus	physical	37.7071676	-2.9390896	\N	\N	12
3055	Ferretería Lallana	physical	40.3458137	-4.1004353	\N	https://www.lallanapolpiscinas.es/	12
3056	Ferreteria Galdona	physical	43.280916	-2.2414576	Joxe Mari Korta industrialdea, A6, 20750, Zumaia	https://ferreteriagaldona.es	12
3057	Ferreteria San Jerónimo	physical	37.4218768	-6.1485163	\N	\N	12
3058	De Tot Bosch	physical	42.1998802	2.4990789	\N	\N	12
3059	Royo	physical	41.0524816	-0.127517	Calle José Pardo Sastrón	\N	12
3060	Ferretería Milenium	physical	41.6544323	-4.7088648	\N	\N	12
3061	Ferretería Plaza_2	physical	41.6507449	-4.7127506	\N	\N	12
3062	La Toma	physical	36.7516079	-5.1430501	\N	\N	12
3063	Ferretería Chamartín_1	physical	40.4645321	-3.6945843	\N	\N	12
3064	Paquito	physical	36.7274359	-4.8624621	\N	\N	12
3065	Lampisteria Josep M. Albentosa	physical	41.4032853	2.1353074	\N	\N	12
3066	Modolell	physical	41.4011866	2.1374726	\N	\N	12
3067	Almacenes Antoñanzas	physical	42.595744	-5.575686	\N	\N	12
3068	Ferretería Garsan	physical	43.5381075	-5.6938188	C. Los Andes, 6, BJ, Gijon-Oeste, 33213 Gijón, Asturias, Spain	\N	12
3069	Ferretería La Purísima_1	physical	38.5000804	-5.1448133	Calle Mercado, 7, 14270, Hinojosa del Duque	\N	12
3070	Manuel Rodríguez Acosta	physical	28.6816468	-17.7660818	\N	\N	12
3071	Ferretería Noja	physical	43.4834697	-3.5292075	Avenida de Ris, 22, 39180, Noja	\N	12
3072	Ferretería Garsan_1	physical	43.5381442	-5.6938356	Calle Los Andes, 6	\N	12
3073	Ferretería - cristalería	physical	38.5011814	-5.1450863	Calle Caridad, 26, 14270, Hinojosa del Duque	\N	12
3074	Romero	physical	42.3510547	-3.665393	\N	\N	12
3075	Ferretería El Puente_1	physical	28.685003	-17.7658981	\N	\N	12
3076	As Breas	physical	42.8232882	-9.0887474	\N	\N	12
3077	Ferreteria_14	physical	40.403889	-3.7143534	Paseo de Juan Antonio Vallejo-Nájera Botas, 48	\N	12
3078	García Fabero	physical	42.7695541	-6.623455	\N	\N	12
3079	Me falta un tornillo	physical	40.3913846	-3.7426644	\N	\N	12
3088	Leroy Merlin_33	physical	\N	\N	\N	\N	12
3089	Leroy Merlin_34	physical	\N	\N	\N	\N	12
3090	Leroy Merlin_35	physical	\N	\N	\N	\N	12
3091	Leroy Merlin_36	physical	\N	\N	Avinguda de la Marina, 17	https://www.leroymerlin.es/	12
3092	Leroy Merlin_37	physical	\N	\N	\N	\N	12
3093	Leroy Merlin_38	physical	\N	\N	\N	\N	12
3094	An de Juan_1	physical	\N	\N	Carretera de Galapagar a Villalba, km. 1	http://www.ajcenter.es/	12
3095	Obramat_9	physical	\N	\N	Avenida de los Rosales, 24	https://www.obramat.es/	12
3096	Leroy Merlin_39	physical	\N	\N	Alcalá de Henares	\N	12
3097	Leroy Merlin_40	physical	\N	\N	46120, Alboraia	https://www.leroymerlin.es/tiendas/alboraya.html	12
3098	Leroy Merlin_41	physical	\N	\N	\N	\N	12
3099	Leroy Merlin_42	physical	\N	\N	\N	\N	12
3100	Leroy Merlin_43	physical	\N	\N	Alcorcón	\N	12
3102	Materiales de construcción Villar	physical	\N	\N	\N	\N	12
3103	Bricocentro_1	physical	\N	\N	\N	\N	12
3104	BricoCentro_4	physical	\N	\N	\N	\N	12
3105	Brico Dépôt_3	physical	\N	\N	Alcalá de Henares	\N	12
3106	Zelai	physical	\N	\N	\N	\N	12
3107	Leroy Merlin_44	physical	\N	\N	\N	\N	12
3108	Fenorte	physical	\N	\N	\N	\N	12
3109	Bauhaus_2	physical	\N	\N	Carrer Victoria Gasteiz, 17003, Girona	https://www.bauhaus.es/	12
3110	Arrona Hermanos	physical	\N	\N	\N	\N	12
3111	Leroy Merlin_45	physical	\N	\N	\N	\N	12
3112	Bauhaus_3	physical	\N	\N	\N	\N	12
3113	Leroy Merlin_46	physical	\N	\N	Carrer de Josep Maria Folch i Torres, 43120, Tarragona	\N	12
3114	Brico Depot	physical	\N	\N	\N	\N	12
3115	Akí	physical	\N	\N	Calle de Luis Buñuel, 18197, Pulianas	https://www.aki.es	12
3116	Leroy Merlin_47	physical	\N	\N	\N	\N	12
3117	Bauhaus_4	physical	\N	\N	Calle Palencia, 3, 29004, Málaga	https://www.bauhaus.es/	12
3118	Leroy Merlin_48	physical	\N	\N	\N	\N	12
3119	Leroy Merlin_49	physical	\N	\N	\N	\N	12
3120	Bauhaus_5	physical	\N	\N	Calle de Campezo, 12, 28022, Madrid	https://www.bauhaus.es/	12
3121	Jomasa	physical	\N	\N	\N	\N	12
3122	Gran La Bañeza	physical	\N	\N	\N	\N	12
3123	Antonio Cuellar	physical	\N	\N	\N	\N	12
3124	Almacenes Roymo	physical	\N	\N	\N	\N	12
3125	Ferrobox_3	physical	\N	\N	\N	\N	12
3126	El Parque	physical	\N	\N	Llanes	\N	12
3162	Pedros	physical	\N	\N	carretera de Moraira a Calpe, 236, 03724, Moraira	\N	12
3163	BricoCentro Paradelo	physical	\N	\N	\N	\N	12
3164	Leroy Merlin_63	physical	\N	\N	\N	\N	12
3165	Bricodepot	physical	\N	\N	\N	\N	12
3168	Leroy Merlin_65	physical	\N	\N	\N	\N	12
3169	Ferreteria Tias	physical	\N	\N	\N	\N	12
3170	Leroy Merlin_66	physical	\N	\N	Calle Me Falta un Tornillo, 3, 47195, Arroyo de la Encomienda	\N	12
3171	Leroy Merlin_67	physical	\N	\N	12A	\N	12
3172	Materiales de Construcción Río Sieira	physical	\N	\N	\N	\N	12
3173	Pivita	physical	\N	\N	\N	\N	12
3174	Nofre S.A.	physical	\N	\N	Ctra. de la Sènia s/n	\N	12
3175	Centro comercial Ferri	physical	\N	\N	Avenida de la Paz, 35, 03400, Villena	\N	12
3176	Ermont, CL	physical	\N	\N	\N	\N	12
3177	Prodelec	physical	\N	\N	carrer Octavi Lecante, 8-10, 08100	\N	12
3178	Brico Dépôt_7	physical	\N	\N	carrer La Bassa, 08150, Parets del Vallès	\N	12
3179	Bonany	physical	\N	\N	\N	\N	12
3180	Pinturex	physical	\N	\N	\N	\N	12
3181	Bricolaje José Carlos	physical	\N	\N	\N	\N	12
3191	Cooperativa	physical	\N	\N	\N	\N	12
3192	BigMat_9	physical	\N	\N	\N	\N	12
3193	Leroy Merlin_69	physical	\N	\N	Carrer de Dinamarca, 4, 08917	\N	12
3194	Aki_2	physical	\N	\N	\N	https://www.leroymerlin.es/aki-leroy-merlin	12
3195	BigMat_10	physical	\N	\N	\N	\N	12
3196	Gyemo Almacén de material eléctrico	physical	\N	\N	\N	\N	12
3197	Brico Dépôt_8	physical	\N	\N	\N	\N	12
3198	Leroy Merlin Alcalá de Guadaíra_1	physical	\N	\N	Alcalá de Guadaíra	\N	12
3199	Leroy Merlin_70	physical	\N	\N	Carrer Medi Ambient, 1, 46470	\N	12
3200	Loibar	physical	\N	\N	\N	\N	12
3201	DONCEL	physical	\N	\N	\N	\N	12
3202	Consydecor	physical	\N	\N	Carretera a Barbarroja, 03689, Hondón de los Frailes	https://consydecor.com/	12
3203	Luces Iluminacion	physical	\N	\N	Avenida Primero de Mayo, 9, 39011, Santander	\N	12
3204	Balaguer	physical	\N	\N	\N	\N	12
3205	Brico Dépôt_9	physical	\N	\N	\N	\N	12
3206	Leroy Merlin_71	physical	\N	\N	\N	\N	12
3207	El Motor II	physical	\N	\N	\N	\N	12
3208	Bauhaus_7	physical	\N	\N	\N	https://www.bauhaus.es	12
3209	Brico Dépôt_10	physical	\N	\N	\N	\N	12
3210	Obramat_10	physical	\N	\N	\N	https://www.bricomart.es	12
3211	Obramat_11	physical	\N	\N	\N	https://www.bricomart.es	12
3212	Almacén de Construcción Cosdresal	physical	\N	\N	Carretera de Coria, 26	\N	12
3213	Ferretería Luis Calvo	physical	\N	\N	\N	\N	12
3214	Delcar	physical	\N	\N	\N	\N	12
3215	Würth_11	physical	\N	\N	\N	\N	12
3227	Leroy Merlin_73	physical	\N	\N	\N	\N	12
3228	Ramos - Suministros	physical	\N	\N	\N	\N	12
3229	Basar Costa Brava	physical	\N	\N	\N	\N	12
3230	Ferretería UCEM	physical	\N	\N	\N	\N	12
3231	BigMat Menditxuri	physical	\N	\N	carretera Leiza, 53, 31740, Doneztebe/Santesteban	https://menditxuri.bigmat.es/site	12
3232	Plataforma de la Construcción	physical	\N	\N	\N	\N	12
3233	Tacha Blanca	physical	\N	\N	\N	\N	12
3234	Bauhaus_8	physical	\N	\N	\N	\N	12
3235	Brico Dépôt_12	physical	\N	\N	\N	\N	12
3236	Bricopinares_1	physical	\N	\N	Calle la Dehesa, 3, 09670	\N	12
3237	Furriols	physical	\N	\N	\N	\N	12
3238	Dogar Material Construcción Bricolaje	physical	\N	\N	Carrera de las Angustias, 62, 29740, Torre del Mar	http://www.dogar.com.es/	12
3272	Derribos Delta	physical	\N	\N	\N	\N	12
3273	Ferreteria Alberola	physical	\N	\N	\N	\N	12
3274	Ferrolan	physical	\N	\N	Carretera de la Roca, 5.6	https://ferrolan.es/	12
3275	Ferretería Barrios Fernández	physical	\N	\N	\N	\N	12
3276	BricoCentro_5	physical	\N	\N	Carretera de Valladolid, 33, 37184, Villares de la Reina	http://www.bricoaguilar.es/	12
3277	Can Pep Bou	physical	\N	\N	\N	\N	12
3278	Ferretería Hibosa	physical	\N	\N	\N	\N	12
3279	Mainca	physical	\N	\N	\N	\N	12
3280	Maderas Bricolaje Valeriano Sierra	physical	\N	\N	Calle Valdemorillo, 8, 28805, Alcalá de Henares	\N	12
3281	es Brico	physical	\N	\N	\N	\N	12
3282	Torrandell	physical	\N	\N	\N	\N	12
3283	Plomer	physical	\N	\N	\N	\N	12
3284	Vilanova	physical	\N	\N	\N	\N	12
3285	Prefabricats Jupe	physical	\N	\N	\N	\N	12
3286	Can Tonió	physical	\N	\N	\N	\N	12
3287	Tocosa	physical	\N	\N	\N	\N	12
3288	Ferretería SAR	physical	\N	\N	Rúa dos Anxos, 50, 15624, Ares	\N	12
3289	Brico Dépôt_16	physical	\N	\N	\N	\N	12
3290	Morlà Mascaró	physical	\N	\N	\N	\N	12
3291	Pallicer Pons	physical	\N	\N	\N	\N	12
3292	Es Brico_2	physical	\N	\N	\N	\N	12
3293	Elektra Catalunya Manresa	physical	\N	\N	Carrer de Castelladral	https://www.grupoelektra.es/	12
3294	Martosa	physical	\N	\N	\N	\N	12
3295	Obramat_12	physical	\N	\N	\N	https://www.bricomart.es	12
3296	Leroy Merlin_77	physical	\N	\N	Calle de Trafalgar, 19004, Guadalajara	https://www.leroymerlin.es/tiendas/compact-guadalajara	12
3297	Brico Serrablo	physical	\N	\N	Avenida de Biescas, 22600, Sabiñánigo	\N	12
3298	Leroy Merlin_78	physical	\N	\N	\N	\N	12
3299	Leroy Merlin_79	physical	\N	\N	\N	\N	12
3300	Construcción Moderna	physical	\N	\N	\N	\N	12
3326	Bricobaeza	physical	\N	\N	Calle Genil, 31A, 23440, Baeza	\N	12
3327	prefabricats Pastor	physical	\N	\N	\N	\N	12
3328	Brico Dépôt_17	physical	\N	\N	\N	\N	12
3266	Jasa	physical	\N	\N	\N	\N	12
3267	Leroy Merlin_75	physical	\N	\N	Carrertera de Rubí, 7, 08174, Sant Cugat del Vallès	\N	12
3268	Pavimentos Castillo	physical	\N	\N	\N	\N	12
3269	Lladó	physical	\N	\N	\N	\N	12
3270	Leroy Merlin_76	physical	\N	\N	Calle de Laguardia, 4, 28022, Madrid	\N	12
3271	BricoCentro Leal	physical	\N	\N	\N	\N	12
3301	Can Binimelis	physical	\N	\N	\N	\N	12
3302	Vibroaspre S.A.	physical	\N	\N	\N	\N	12
3303	Ferretería Rocha	physical	\N	\N	\N	\N	12
3304	Grupo AGROCENTRO	physical	\N	\N	Calle Poniente, 24, 23470, Cazorla	\N	12
3305	Cerrajeria Antonio Marin y dos mas C.B.	physical	\N	\N	Calle Levante, 34, 23470, Cazorla	\N	12
3306	Seguina	physical	\N	\N	\N	\N	12
3307	materials Pol Amengual	physical	\N	\N	\N	\N	12
3308	Leroy Merlin_80	physical	\N	\N	\N	\N	12
3309	Feruser	physical	\N	\N	\N	\N	12
3310	Ferretería Albaladejo	physical	\N	\N	\N	\N	12
3311	Grupo Schröder	physical	\N	\N	Carretera C-17, 16.667	\N	12
3312	Leroy Merlin_81	physical	\N	\N	\N	\N	12
3313	Magatzem ses Forques	physical	\N	\N	\N	\N	12
3314	Biedma Campos Hermanos	physical	\N	\N	23400, Úbeda	\N	12
3315	Ferretería Ubetense	physical	\N	\N	23400, Úbeda	\N	12
3316	Almacenes San Blas	physical	\N	\N	Calle Santo Domingo, 21200, Aracena	http://www.almacenes-sanblas.com/	12
3317	Agrijardi	physical	\N	\N	Carrer dels Freixes, 17133, Serra de Daró	\N	12
3318	Leroy Merlin_82	physical	\N	\N	\N	\N	12
3319	Ferretería La Montañesa	physical	\N	\N	Avenida de Candina, 7, 39011, Santander	\N	12
3320	Leroy Merlin_83	physical	\N	\N	Carretera de Palma del Río	https://www.leroymerlin.es	12
3321	Würth_12	physical	\N	\N	\N	\N	12
3322	Obramat_13	physical	\N	\N	\N	https://www.bricomart.es	12
3323	materials Tucasa	physical	\N	\N	\N	\N	12
3324	Baix de la Vila	physical	\N	\N	\N	\N	12
3325	Leroy Merlin_84	physical	\N	\N	Badajoz	\N	12
3372	Suministros Villaviciosa S.L.	physical	\N	\N	Avenida de América, 16, 28922, Alcorcón	\N	12
3373	Leroy Merlin_89	physical	\N	\N	Barrio Peruri, 33, 48940, Leioa - Lejona	https://www.leroymerlin.es/	12
3374	Regueiro	physical	\N	\N	\N	\N	12
3375	Leroy Merlin_90	physical	\N	\N	Puerto Real	\N	12
3384	Saltoki Galdakao	physical	\N	\N	Pol. Guturribai, Calle Gernika, 46, Nave B1, 48960, Galdakao	https://www.saltoki.com/	12
3385	Leroy Merlin_93	physical	\N	\N	\N	\N	12
3386	Materials Verger	physical	\N	\N	\N	\N	12
3387	Leroy Merlin_94	physical	\N	\N	\N	\N	12
3388	Ferretería Martín_1	physical	\N	\N	\N	\N	12
3389	Bauhaus_11	physical	\N	\N	Calle Sector 1 Ab, 2F, 46910	\N	12
3390	La Constructora	physical	\N	\N	Carrer del Doctor Vicent Segura, 4, 46600, Alzira	http://www.materiales-laconstructora.com/	12
3391	Ferretería Pilasan	physical	\N	\N	\N	\N	12
3392	Leroy Merlin_95	physical	\N	\N	\N	\N	12
3393	Leroy Merlin Compact_1	physical	\N	\N	\N	\N	12
3394	El Canario	physical	\N	\N	Avenida Ciudad de Guadix, 14A, 18500, Guadix	\N	12
3395	Meraya	physical	\N	\N	18500, Guadix	http://www.meraya.net	12
3396	El Metal	physical	\N	\N	\N	\N	12
3397	La Lupa	physical	\N	\N	\N	\N	12
3398	Suministros Lavín	physical	\N	\N	Calle de Alday, 39600, Maliaño	https://suministroslavin.com/	12
3399	Longo	physical	\N	\N	\N	\N	12
3407	El Almacén Shop	physical	\N	\N	Avinguda de Barcelona, 168, 43892, Mont-roig del Camp	http://www.elalmacenshop.com/	12
3408	Ferretería Valle Sur	physical	\N	\N	\N	\N	12
3409	BriCor_6	physical	\N	\N	\N	\N	12
3410	Aguilar_1	physical	\N	\N	Avenida do Marqués de Figueroa, 102-104, 15500, Fene	\N	12
3452	Adrover Joyma	physical	\N	\N	\N	\N	12
3453	Ferretería Ferrafas	physical	\N	\N	\N	\N	12
3454	Leroy Merlin_103	physical	\N	\N	Avenida de la Constitución, 102, 28850, Torrejón de Ardoz	https://www.leroymerlin.es/tiendas/compact-torrejon.html	12
3455	Obramat Santander	physical	\N	\N	Calle de la Peseta, 5, 39011, Santander	https://www.obramat.es/	12
3456	Würth_14	physical	\N	\N	Carrer de la Múnia, 36, 08720, Vilafranca del Penedès	https://www.wurth.es	12
3457	Fenorte Trespa	physical	\N	\N	\N	\N	12
3458	Hilti_2	physical	\N	\N	Carretera de Villaverde a Vallecas, 259	\N	12
3459	Obramat_20	physical	\N	\N	Avinguda del Conflent, 08915, Badalona	\N	12
3465	Soberats	physical	\N	\N	\N	\N	12
3466	Doniz	physical	\N	\N	\N	\N	12
3467	Marcial	physical	\N	\N	\N	\N	12
3468	HM Matas García	physical	\N	\N	Carretera de Béjar, Sanchotello	\N	12
3469	Leroy Merlin_104	physical	\N	\N	\N	\N	12
3470	Ferreteria Maranges	physical	\N	\N	\N	\N	12
3471	Ferreteria Bacarisas	physical	\N	\N	\N	https://bacarisas.com/	12
3472	Leroy Merlin_105	physical	\N	\N	\N	\N	12
3473	Derribos Andrés	physical	\N	\N	\N	\N	12
3474	Mercaderribo	physical	\N	\N	\N	\N	12
3475	Alorda	physical	\N	\N	\N	\N	12
3476	Ballester Palou	physical	\N	\N	\N	\N	12
3477	Planisi	physical	\N	\N	\N	\N	12
3478	Fercon	physical	\N	\N	\N	\N	12
3479	materials Antònia	physical	\N	\N	\N	\N	12
3480	Maderas Francisco Sánchez Orcera	physical	\N	\N	Calle Solería, 23400, Úbeda	\N	12
3481	Obramat_21	physical	\N	\N	\N	https://www.bricomart.es	12
3482	Ferretería Pepín	physical	\N	\N	Calle Aldea, 2, 38570	\N	12
3483	Leroy Merlin_106	physical	\N	\N	Avinguda de la Generalitat, Tortosa	\N	12
3484	Sobrino G	physical	\N	\N	\N	https://sobrinog.com/	12
3485	Bricolage Bazán	physical	\N	\N	Avenida Málaga Oloroso, 42, 29014	\N	12
3486	Furroy	physical	\N	\N	\N	\N	12
3487	Obramat_22	physical	\N	\N	\N	https://www.bricomart.es	12
3488	Almacén Casa Calvo	physical	\N	\N	\N	\N	12
3489	Ricardo Ferreteria	physical	\N	\N	\N	\N	12
3490	Obramat_23	physical	\N	\N	\N	https://www.bricomart.es	12
3491	BricoMarian	physical	\N	\N	\N	\N	12
3492	Ferreteria Genis Pujol	physical	\N	\N	\N	\N	12
3493	BricoMax - Cadena 88	physical	\N	\N	Carretera Mazarambroz, 4, 45100, Sonseca	\N	12
3494	Electro Molina_1	physical	\N	\N	Avinguda Puigdomí	\N	12
3495	Ferretería Rodes	physical	\N	\N	\N	\N	12
3496	Distone	physical	\N	\N	\N	\N	12
3497	Toni Capó	physical	\N	\N	58	\N	12
3511	Ferxaouen	physical	\N	\N	Ronda de los Olivares, 49, 23009, Jaén	\N	12
3512	Grupo Noguerol	physical	\N	\N	\N	https://www.gruponoguerol.com/	12
3513	Brico Sant Celoni	physical	\N	\N	\N	\N	12
3514	Comercial Escallada	physical	\N	\N	Calle de José Estrañi, 5G, 39011, Santander	\N	12
3515	BigMat_13	physical	\N	\N	\N	\N	12
3548	FesMés	physical	\N	\N	\N	\N	12
3549	Igartua	physical	\N	\N	Akarregi, 2C, 20120, Hernani	\N	12
3550	Ferreterias Droguemar	physical	\N	\N	Avenida de la Aduana, 18, 04740, Roquetas de Mar	\N	12
3329	Ferretería Ortiz_2	physical	\N	\N	\N	\N	12
3330	La Herramienta Balear_1	physical	\N	\N	\N	\N	12
3331	materials Fullana	physical	\N	\N	\N	\N	12
3332	Obramat_14	physical	\N	\N	\N	\N	12
3333	Can Bauçà	physical	\N	\N	\N	\N	12
3334	Porcelanosa_1	physical	\N	\N	Avenida de Parayas, 48, 39011, Santander	https://www.porcelanosa.com/	12
3335	Alufasa	physical	\N	\N	Calle del Concejo, 17, 39011, Santander	https://www.alufasa.com/	12
3336	Materials Magripalma	physical	\N	\N	\N	\N	12
3337	Madriferr	physical	\N	\N	Calle Elvas, 3, Leganés	\N	12
3338	Sánchez_3	physical	\N	\N	\N	\N	12
3339	ObraMart Leganés	physical	\N	\N	Avenida Puerta del Sol, 2, 28918, Leganés	\N	12
3340	Autoluz Samaniego	physical	\N	\N	Calle de la Tejera, 8, 39012, Santander	\N	12
3341	Canaima_1	physical	\N	\N	Camiño Basanta	http://www.canaima.es/	12
3342	Induhogar	physical	\N	\N	Calle José Lastiesas, 22600, Sabiñánigo	\N	12
3343	Disfersa	physical	\N	\N	Plaza de Azpe, 1, 22600, Sabiñánigo	\N	12
3344	Apatel	physical	\N	\N	\N	\N	12
3345	Can Bibi	physical	\N	\N	\N	\N	12
3346	Ferretería Pedro Durán	physical	\N	\N	\N	\N	12
3347	Leroy Merlin_85	physical	\N	\N	\N	\N	12
3348	Cámara	physical	\N	\N	\N	https://www.grupocamara.es/	12
3349	Calleja	physical	\N	\N	\N	\N	12
3350	Ferretería Jaca S.L.	physical	\N	\N	Carretera General Icod-Buenavista, 38470, Los Silos	\N	12
3351	Brico Dépôt_18	physical	\N	\N	\N	\N	12
3352	Leroy Merlin_86	physical	\N	\N	Avenida San Rafael, 18006, Armilla	\N	12
3353	Bricomat_1	physical	\N	\N	Calle Estocolmo, 1, 42110, Ólvega	\N	12
3354	Leroy Merlín	physical	\N	\N	\N	\N	12
3355	Brico Dépôt_19	physical	\N	\N	Avinguda de la Llibertat, 1, 46600, Alzira	https://www.bricodepot.es/tiendas/brico-depot-alzira	12
3356	FerreMar	physical	\N	\N	\N	\N	12
3357	BigMat Dismar	physical	\N	\N	\N	https://dismar.bigmat.es/	12
3358	Ferretería La Jarilla	physical	\N	\N	\N	\N	12
3359	Ferretería Berto	physical	\N	\N	Estrada da Palma, 74, 15528, Fene	\N	12
3360	Suministros Monte	physical	\N	\N	Calle de Bolado, 40, 39012, Santander	https://suministrosmonte.com	12
3361	BricoCentro_6	physical	\N	\N	\N	https://www.bricocentroaranda.es/	12
3362	Bricosyl	physical	\N	\N	Rúa de Eslovaquia, 8, 15707, Santiago de Compostela	\N	12
3363	Leroy Merlin_87	physical	\N	\N	\N	https://www.leroymerlin.es/	12
3364	Leroy Merlin_88	physical	\N	\N	Palmones	\N	12
3365	Alkain	physical	\N	\N	Txalaka pasealekua, 23, 20115, Astigarraga	https://www.alkain.com/	12
3366	Comercial Diresa	physical	\N	\N	\N	\N	12
3367	Würth_13	physical	\N	\N	\N	\N	12
3368	Cal Sutracas	physical	\N	\N	\N	\N	12
3369	Ferretería La Llave_4	physical	\N	\N	Avenida de Mugardos, 6, 15624, Ares	\N	12
3370	Chambalo	physical	\N	\N	Avenida Valladolid-Soria	\N	12
3371	Obramat_15	physical	\N	\N	\N	https://www.bricomart.es	12
3376	Cas Picapedrer	physical	\N	\N	\N	\N	12
3377	Obramat_16	physical	\N	\N	Calle Armada Española, 28922, Alcorcón	https://www.bricomart.es	12
3378	Bauhaus_10	physical	\N	\N	Calle Ejército del Aire, 28922, Alcorcón	https://www.bauhaus.es/es/nuestros-centros	12
3379	Ferreteria Puig Industrial	physical	\N	\N	\N	\N	12
3380	BricoCentro Extremeño	physical	\N	\N	Avenida Juan Carlos Rodríguez Ibarra, 291, 06200, Almendralejo	\N	12
3381	Leroy Merlin_91	physical	\N	\N	Carrer de Maria Callas, 2, 43883, Roda de Berà	\N	12
3382	Leroy Merlin_92	physical	\N	\N	\N	\N	12
3383	Azumay	physical	\N	\N	\N	\N	12
3400	Antioquia 2008	physical	\N	\N	\N	\N	12
3401	Ferretería Tahíche	physical	\N	\N	\N	\N	12
3402	Comercial Gómez	physical	\N	\N	Costa de San Marcos, 11	\N	12
3403	Brico Galicia	physical	\N	\N	Costa de San Marcos, 9	\N	12
3404	Ferreteria Industrial FER3	physical	\N	\N	Carrer del Loira, 44, 43870, Amposta	\N	12
3405	Adrover	physical	\N	\N	\N	\N	12
3406	Ferretería SAR_1	physical	\N	\N	\N	\N	12
3411	Comercial Agrícola Cuanda	physical	\N	\N	\N	\N	12
3412	Leroy Merlin_96	physical	\N	\N	\N	\N	12
3413	Saneamientos Feral	physical	\N	\N	\N	\N	12
3414	Almacén de Ferretería Manuel Álvarez	physical	\N	\N	\N	\N	12
3415	Unión Ferretera	physical	\N	\N	\N	\N	12
3416	Leroy Merlin_97	physical	\N	\N	Camí dels Rolls, 46500, Sagunto	\N	12
3417	materials Tomeu Bo	physical	\N	\N	\N	\N	12
3418	Ceycesa	physical	\N	\N	\N	\N	12
3419	Gres y Azulejos Galapagar	physical	\N	\N	Calle Ramona, 50	https://www.gresyazulejosgalapagar.es/es/	12
3420	Arcoisa Piscinas	physical	\N	\N	Calle de Serranillo, 14	https://www.arcoisa.es/	12
3421	Bricomat_2	physical	\N	\N	\N	\N	12
3422	Obramat_17	physical	\N	\N	Avenida Manuel Castillo, 29004	https://www.bricomart.es/nuestros-almacenes/bm-malaga.html	12
3423	Ferreteria Garcia	physical	\N	\N	\N	\N	12
3424	Obramat_18	physical	\N	\N	\N	https://www.bricomart.es	12
3425	Amigó	physical	\N	\N	\N	\N	12
3426	Dyreco	physical	\N	\N	\N	\N	12
3427	Fibrotec	physical	\N	\N	\N	\N	12
3428	Brico Dépôt_20	physical	\N	\N	Carrer Satsuma, 1, 12539, les Alqueries / Alquerías del Niño Perdido	\N	12
3429	Suinbal	physical	\N	\N	\N	\N	12
3430	Leroy Merlin_98	physical	\N	\N	Carretera de Madrid, 114, 45600, Talavera de la Reina	\N	12
3431	Bauhaus_12	physical	\N	\N	\N	\N	12
3432	Leroy Merlin_99	physical	\N	\N	\N	\N	12
3433	Bricomart Jinámar	physical	\N	\N	\N	\N	12
3434	Brico López	physical	\N	\N	Calle Vente Vacío, 04628, Antas	https://lopezferreteria.es/	12
3435	Ferremat Ferretería	physical	\N	\N	Palomares	\N	12
3436	Leroy Merlin Compact Torrelavega	physical	\N	\N	Avenida de Bilbao, 124, 39300, Sierrapando	\N	12
3437	Ferretería Juan Gonzáles Parra	physical	\N	\N	\N	\N	12
3438	Ferretería Trasierra	physical	\N	\N	\N	\N	12
3439	Leroy Merlin_100	physical	\N	\N	Lintzirin Poligonoa, 12, 20180, Oiartzun	\N	12
3440	Almacén de Materiales Benigno García	physical	\N	\N	Carretera Aldehuela, 12, 37600, Tamames	\N	12
3441	Obramat_19	physical	\N	\N	Avenida de Galicia, Carbajosa de la Sagrada	https://www.bricomart.es	12
3442	Leroy Merlin_101	physical	\N	\N	\N	\N	12
3443	Ferretería Cartelle	physical	\N	\N	Rúa Catavento, B2, 2, 15500, Fene	https://www.ferreteriacartelle.es/	12
3444	Ferrokey Sánchez Filio Industrial	physical	\N	\N	Avenida del Príncipe de Asturias, 103,105, 28670, Villaviciosa de Odón	https://www.ferrokey.eu/ferrokey-villaviciosa	12
3445	Calvià 2	physical	\N	\N	\N	\N	12
3446	Elig Bricolage y Pinturas	physical	\N	\N	calle Pedro Juan Perpinyán, 100, 03204, Elche/Elx	\N	12
3447	VIII Milla, S.L.	physical	\N	\N	Calle Dinamarca, 64, 50180, Utebo	\N	12
3448	Mas Guait	physical	\N	\N	\N	\N	12
3449	construcciones Méndez	physical	\N	\N	\N	\N	12
3450	Justo Otero e Hijos, SL	physical	\N	\N	Avenida Mendiño, 23, 36800	https://justotero.com/	12
3451	Leroy Merlin_102	physical	\N	\N	Carrer d'Astúries, 66, 17003, Girona	\N	12
3460	Ferreteria Postigo	physical	\N	\N	\N	\N	12
3461	BigMat_11	physical	\N	\N	\N	\N	12
3462	Roycha_3	physical	\N	\N	Calle Valle de Manzanedo, 1	\N	12
3463	Ferretería La Paz	physical	\N	\N	Calle Ibsen, 17, 29004	\N	12
3464	OPTIMUS	physical	\N	\N	\N	\N	12
3498	Leroy Merlin_107	physical	\N	\N	\N	\N	12
3499	Eurosur Sanlúcar	physical	\N	\N	Calle Fray Isidro de Sevilla, 3, 11540, Sanlúcar de Barrameda	https://www.eurosursanlucar.com/	12
3500	Obramat_24	physical	\N	\N	Calle La Flauta Mágica, 25, 28222, Majadahonda	https://www.obramat.es/	12
3501	Ferreteria Hidraulicas Talavera	physical	\N	\N	\N	\N	12
3502	Leroy Merlin_108	physical	\N	\N	\N	\N	12
3503	Ferretería/Muebles Palmanova	physical	\N	\N	\N	\N	12
3504	Hiper Ahorro	physical	\N	\N	\N	\N	12
3505	SRS Técnicas, S.L.	physical	\N	\N	\N	\N	12
3506	BigMat_12	physical	\N	\N	\N	\N	12
3507	Triñanes Suministros Industriales	physical	\N	\N	\N	\N	12
3508	Ferretería Leyma	physical	\N	\N	Avenida de la Constitución, 144, 06640, Talarrubias	\N	12
3509	FERPI	physical	\N	\N	\N	\N	12
3510	Habitacle_1	physical	\N	\N	Carretera d'Artà, 89, 07458	http://habitaclemallorca.com	12
3516	Leroy Merlin_109	physical	\N	\N	\N	\N	12
3517	Ferrocentro Granda	physical	\N	\N	\N	\N	12
3518	Ferreteria Hermanos Pio	physical	\N	\N	Calle Real, 197, La Matanza de Acentejo	http://www.ferreteriahnospio.es	12
3519	Kompas	physical	\N	\N	\N	\N	12
3520	Ferrsada-bricolandia	physical	\N	\N	Avenida de Barrié de la Maza, 15160, Sada	https://www.bricolandia.es/	12
3521	Leroy Mrlin Compact	physical	\N	\N	\N	\N	12
3522	Suministros Hermanos Billete S.l.	physical	\N	\N	\N	\N	12
3523	Leroy Merlin_110	physical	\N	\N	\N	\N	12
3524	Calabuig	physical	\N	\N	\N	\N	12
3525	Fesmés_1	physical	\N	\N	Carrer del Pallars, 2, 08812	\N	12
3526	Leroy Merlin_111	physical	\N	\N	\N	\N	12
3527	Saltoki_1	physical	\N	\N	\N	\N	12
3528	Cuñasa	physical	\N	\N	Carretera Zaragoza, KM 333, 26540, Alfaro	https://www.cunasa.com/	12
3529	Leroy Merlin_112	physical	\N	\N	\N	\N	12
3530	Cuchillería Navarro	physical	\N	\N	\N	https://cuchillerianavarro.com/	12
3531	Consydecor_1	physical	\N	\N	Carretera de Aspe a Los Hondones, 03680, Aspe	https://consydecor.com/	12
3532	Obramat_25	physical	\N	\N	Rúa Durán Loriga Juan Jacobo (matemático), 10, 27003, Lugo	https://www.bricomart.es	12
3533	BigMat_14	physical	\N	\N	\N	\N	12
3534	Ferretería J. Chamorro	physical	\N	\N	\N	\N	12
3535	Ferreteria Martí_2	physical	\N	\N	Carrer de la Tolerància, 16, Reus	\N	12
3536	BigMat_15	physical	\N	\N	\N	\N	12
3537	Torsesa_1	physical	\N	\N	\N	\N	12
3538	Rame	physical	\N	\N	\N	\N	12
3539	Leroy Merlin_113	physical	\N	\N	\N	\N	12
3540	Bricolaje Bueno	physical	\N	\N	\N	\N	12
3541	Leroy Merlin_114	physical	\N	\N	\N	https://www.leroymerlin.es/	12
3542	Saltoki_2	physical	\N	\N	\N	\N	12
3543	Leroy Merlin_115	physical	\N	\N	\N	\N	12
3544	Clickfer	physical	\N	\N	\N	\N	12
3545	Leroy Merlin_116	physical	\N	\N	\N	\N	12
3546	La Parada	physical	\N	\N	\N	\N	12
3547	Comercial Lerma	physical	\N	\N	\N	\N	12
3562	Ferretería Antonio Cobo	physical	\N	\N	\N	\N	12
3573	Ferretería Cancho_1	physical	39.4593764	-6.3727339	Calle Colombia, 6, 10005, Cáceres	\N	12
3577	Leroy Merlin_2	physical	41.6105355	-0.8906721	\N	https://www.leroymerlin.es/	12
3578	Ferreteria_1	physical	36.4897599	-4.7151034	\N	\N	12
3580	Leroy Merlin_4	physical	37.9294082	-0.7369456	\N	\N	12
3582	Ferretería Arenal_1	physical	40.0846237	-3.8763362	\N	\N	12
3587	Ferretería_2	physical	37.9934776	-1.1267232	\N	\N	12
3588	Ferretería_3	physical	38.9180982	-1.9183101	\N	\N	12
3593	Ferretería_4	physical	38.1285259	-0.8771775	\N	\N	12
3596	Leroy Merlin_7	physical	40.5304099	-3.6464256	\N	\N	12
3599	BricoKing_1	physical	43.2999956	-7.6777002	\N	\N	12
3603	Ferretería Alonso_2	physical	40.4880357	-3.6626975	\N	\N	12
3606	Ferreteria Torres_1	physical	41.7431636	1.8041627	\N	\N	12
3608	Ferretería_5	physical	39.3373499	-5.4899236	\N	\N	12
3615	Rigau_1	physical	41.9820005	2.8179819	\N	\N	12
3616	Servei Estació_1	physical	41.9831182	2.8192567	Carrer de la Sèquia, 20, 17001, Girona	\N	12
3618	Ferreteria_3	physical	27.9018013	-15.4466066	\N	\N	12
3619	Würth_1	physical	43.4514614	-3.8352109	\N	https://www.wurth.es/	12
3620	La Llave_1	physical	38.7609449	-3.387322	Calle de las Escuelas, 57, 13300, Valdepeñas	\N	12
3621	Suministros Valdepeñas_1	physical	38.7680012	-3.3882501	Avenida de Gregorio Prieto, 35, 13300, Valdepeñas	\N	12
3622	Comercial MHM_1	physical	40.8280489	-5.5136517	\N	\N	12
3625	Roycha_1	physical	42.3630116	-3.7515965	Calle Condado de Treviño, 4, 09001, Burgos	\N	12
3626	Torres_1	physical	38.25471	-3.1312625	\N	\N	12
3627	Contaval automatismos y componentes electrónicos, S.L._1	physical	40.4329929	-3.6082298	Calle de María Sevilla Diago, 16	https://www.contaval.es/	12
3628	Ferretería Avenida_1	physical	40.2067911	-3.5786041	\N	\N	12
3631	Leroy Merlin_14	physical	37.1448937	-3.6131644	18100, Armilla	https://www.leroymerlin.es	12
3638	El Hórreo_1	physical	42.8761214	-8.5441099	Rúa do Hórreo, 22, 15701, Santiago de Compostela	\N	12
3639	Ferretería Cancho_2	physical	39.4857426	-6.3641727	\N	\N	12
3640	Venecia_3	physical	40.4347971	-3.7037008	\N	\N	12
3641	Leroy Merlin_16	physical	43.3434588	-8.4284753	Estrada dos Baños de Arteixo, 43, 15008, A Coruña	https://www.leroymerlin.es/	12
3642	Ferreteria_4	physical	40.2102326	-3.5716888	\N	\N	12
3644	Amado Cárdenes, Maquianaria de Hostelería_1	physical	28.1097431	-15.4174422	\N	\N	12
3645	Amado Cárdenes, Maquianaria de Hostelería_2	physical	28.1099762	-15.4169194	\N	\N	12
3646	Optimus_2	physical	28.9729615	-13.564081	\N	\N	12
3647	7 Islas, Pintura_1	physical	28.1169828	-15.4230301	\N	\N	12
3648	Ferrymas_1	physical	41.6520856	-0.9098091	\N	\N	12
3650	Roycha_2	physical	42.3450286	-3.6894671	Calle Briviesca, 34, 09004, Burgos	www.casataller.es	12
3651	Ferretería Sánchez_2	physical	36.8436366	-2.4470517	04006	\N	12
3652	Leroy Merlin_17	physical	41.3873539	2.0400466	Carretera de Laureà Miró, 361, 08980, Sant Feliu de Llobregat	\N	12
3653	El Martillo_1	physical	36.837157	-2.4580336	\N	\N	12
3659	BigMat_1	physical	36.2805415	-6.0895224	\N	\N	12
3660	Riosmat BigMat_1	physical	41.0089984	-6.4387296	\N	https://www.riosmat.bigmat.es/	12
3661	Optimus_3	physical	39.6027668	3.3827544	\N	\N	12
3551	Adasa	physical	\N	\N	\N	\N	12
3552	CIVERPLAST	physical	\N	\N	Carretera de Alicún, 04740, Roquetas de Mar	\N	12
3553	FYSASUR	physical	\N	\N	\N	\N	12
3554	Ferretería Morala	physical	\N	\N	\N	\N	12
3555	Valeriano	physical	\N	\N	\N	\N	12
3556	Ferreteria Ribadavia	physical	\N	\N	\N	\N	12
3557	Home Markt	physical	\N	\N	\N	\N	12
3558	Bauhaus_13	physical	\N	\N	\N	\N	12
3559	Leroy Merlin_117	physical	\N	\N	\N	\N	12
3560	El bazar	physical	\N	\N	\N	\N	12
3561	Ferretería Casa Lado	physical	\N	\N	Praza da Constitución, 19, 15270, Cee	\N	12
3563	Ferretería Badajoz	physical	\N	\N	Avenida de Aragón, 18, 28903, Getafe	\N	12
3564	Bauhaus_14	physical	\N	\N	Carrer de Cartagena, 11, 17005, Girona	\N	12
3565	Leroy Merlin_118	physical	\N	\N	\N	\N	12
3566	Azulejos y sanitarios García Escudero	physical	\N	\N	\N	\N	12
3567	Hermanos Rodríguez Almacén	physical	\N	\N	\N	\N	12
3568	Placo Saint-Gobain	physical	\N	\N	\N	\N	12
3569	Leroy Merlin_119	physical	\N	\N	\N	\N	12
3570	Leroy Merlin_120	physical	\N	\N	Camino de la Paloma, 25, 30150, La Alberca	https://www.leroymerlin.es/	12
3571	materials Can Fiol	physical	\N	\N	\N	\N	12
3572	Terrapilar	physical	\N	\N	\N	\N	12
3574	Leroy Merlin_1	physical	38.0381689	-1.1517418	\N	\N	12
3575	Carpinteria metálica "Hermanos Soto"_1	physical	37.9983114	-3.4733293	\N	\N	12
3576	Construcciones "Marjisur 2005"_1	physical	37.9983283	-3.4730651	\N	\N	12
3579	Leroy Merlin_3	physical	43.4284465	-3.8401569	\N	\N	12
3581	Almacén Domingo_1	physical	41.4491936	-5.72834	\N	\N	12
3583	Leroy Merlin_5	physical	39.4996685	-0.4086807	Avenida de la Ilustración, 6, 46100, València	\N	12
3584	Ferretería_1	physical	40.3884486	-3.7662737	\N	\N	12
3585	Ferretería Alonso_1	physical	38.0617578	-0.8673765	Avenida de la Paz, 21, Jacarilla	\N	12
3586	Barchafe_1	physical	37.7681922	-3.7891673	Calle San Clemente, 9, 23004	https://barchafe.com/	12
3589	Juanjo_1	physical	38.9958132	-1.8676465	\N	\N	12
3590	Juanjo_2	physical	38.9873406	-1.8531783	\N	\N	12
3591	Brico Dépôt_1	physical	43.5049189	-8.2020871	Centro Comercial de O Boial	\N	12
3592	Leroy Merlin_6	physical	38.9067564	-6.3510687	\N	\N	12
3594	Ferretería Lima_1	physical	43.4586726	-3.8266298	Calle de San Fernando, 88, 39007, Santander	\N	12
3595	Ferretería Lima_2	physical	43.4622426	-3.8373834	Calle de la Albericia, 5A, 39012, Santander	\N	12
3597	Leroy Merlin_8	physical	36.7754227	-2.6131897	Carretera de Alicún, 04740, Roquetas de Mar	\N	12
3598	Ferreteria_2	physical	37.8457854	-3.0679795	\N	\N	12
3600	Ferretería Pascual_1	physical	38.9942955	-1.8630733	\N	\N	12
3601	Leroy Merlin_9	physical	40.4467338	-3.6976548	\N	\N	12
3602	Gogar_1	physical	40.4074313	-3.6497939	Calle de la Marroquina, 15, 28030, Madrid	\N	12
3604	Venecia_1	physical	40.4270456	-3.7014727	\N	\N	12
3605	Leroy Merlin_10	physical	38.7320025	-0.4429448	\N	\N	12
3607	Leroy Merlin_11	physical	41.4412809	2.1989235	Paseo Portesí, 2	https://www.leroymerlin.es	12
3609	La Ferretería_1	physical	37.3436014	-5.9802242	Avenida de Finlandia	\N	12
3610	Ferretería Tropical_1	physical	40.281497	-3.8087044	\N	\N	12
3611	Cadena 88_1	physical	40.4733555	-3.6367587	\N	\N	12
3612	Ferretería_6	physical	38.2606717	-5.6787525	\N	\N	12
3613	Leroy Merlin_12	physical	42.0125357	-4.5184731	Avenida de Brasilia, 5, 34004, Palencia	\N	12
3614	Ferretería Sánchez_1	physical	40.9696312	-5.6654535	Paseo de Carmelitas, 20,22, Salamanca	\N	12
3617	Ferretería_7	physical	40.4182756	-3.5724758	\N	\N	12
3623	Ferretería_8	physical	39.8018876	-5.1735408	\N	\N	12
3624	Ferroisora_1	physical	28.2086392	-16.7777515	\N	\N	12
3629	Leroy Merlin_13	physical	42.1708703	-8.6205928	\N	\N	12
3630	Optimus_1	physical	38.6460472	0.0401922	\N	https://www.optimusferreteria.com/	12
3632	Azulejos Peña_1	physical	40.4860636	-3.6845463	\N	\N	12
3633	Venecia_2	physical	40.4348068	-3.7041313	\N	\N	12
3634	Ferretería Fernández_1	physical	37.7439053	-0.9531847	\N	\N	12
3635	Ferretería Alonso_3	physical	40.4244611	-3.5633369	\N	\N	12
3636	Leroy Merlin_15	physical	41.7232162	1.8481964	Carrer d'Agustí Coll, 2, 08243, Manresa	\N	12
3637	Barchafe_2	physical	37.7735025	-3.7932741	\N	\N	12
3643	Ferreteria_5	physical	38.013852	-1.0353262	\N	\N	12
3649	Ferretería_9	physical	41.0703803	1.1508825	Carrer de Falset, 27, 43840	\N	12
3654	Lamagrande_1	physical	40.4380958	-3.6535919	\N	\N	12
3655	Nueva Ferretería_1	physical	40.4286572	-3.669609	\N	\N	12
3656	La Clau_1	physical	41.9950077	1.5220246	\N	\N	12
3657	Venecia_4	physical	40.4370986	-3.6528671	\N	\N	12
3658	Comercial Metabos_1	physical	40.9913398	-5.6432732	Calzada de Toro, 28	http://www.metabos.com/	12
3662	Ferreteria Abando_1	physical	43.2650185	-2.9309166	\N	\N	12
3663	BriCor_1	physical	39.4848506	-0.3973197	Avinguda de Pius XII, 51, 46015	http://bricor.es	12
3664	Ferretería J. Calles_1	physical	41.0082118	-6.4349183	Calle Honda, 4, 37210, Vitigudino	\N	12
3665	BriCor_2	physical	40.4301735	-3.7161342	\N	\N	12
3666	Ferretería Delgado_1	physical	40.4892538	-3.3574519	Calle Juan de Borgoña, 4	\N	12
3667	Ferretería_10	physical	42.4176324	-4.0428164	\N	\N	12
3668	Ferretería Prosperidad_1	physical	37.3819682	-6.0846164	\N	\N	12
3669	Würth_2	physical	40.9898025	-5.6444615	\N	\N	12
3670	Ferretería San José_1	physical	28.0976894	-15.417886	\N	\N	12
3671	BigMat_2	physical	43.2108532	-8.6917663	\N	\N	12
3672	Campo y Hogar_1	physical	36.2825266	-6.0882489	\N	\N	12
3673	Optimus_4	physical	41.4929357	2.1445302	\N	\N	12
3674	Ferretería Escrig_1	physical	39.9916085	-0.0396927	Calle Ronda Vinatea, 3, 12004	https://www.ferreteriaescrig.es/	12
3675	Ferretería Vidal_1	physical	41.4345433	2.2188529	\N	\N	12
3676	Ferretería_11	physical	41.2129396	1.1404647	\N	\N	12
3677	Aki_1	physical	37.9898503	-0.686998	\N	\N	12
3678	La Ferretería_2	physical	36.0175403	-5.6083757	\N	\N	12
3679	Ferreteria_6	physical	27.7643634	-15.5774746	\N	\N	12
3680	Ferretería Sánchez_3	physical	37.2225194	-3.691065	Avenida de la Estación, 19, 18230, Atarfe	https://www.tuferreteronline.com	12
3681	El Hórreo_2	physical	42.867735	-8.5541045	García Prieto	\N	12
3682	Ferretería Avenida_2	physical	38.6004946	-0.0488306	\N	\N	12
3683	Burgos Ferretería_1	physical	43.3478076	-4.0521167	Calle del Marqués de Santillana, 2, 39300, Torrelavega	\N	12
3684	González_1	physical	36.5102959	-6.278003	\N	\N	12
3685	Ferrymas_2	physical	41.6508433	-0.8775458	\N	\N	12
3686	La Llave_2	physical	38.3834658	-0.7607078	Avenida de la Constitución, 67	\N	12
3687	Würth_3	physical	42.5728899	-5.5301622	\N	\N	12
3688	Ferretería Sánchez_4	physical	28.4272566	-16.3141079	\N	\N	12
3692	Leroy Merlin_18	physical	40.4467768	-3.6981936	Calle de Raimundo Fernández Villaverde, 43, 28003, Madrid	https://www.leroymerlin.es/	12
3693	Ferretería Norte_1	physical	28.6861545	-17.7608588	\N	\N	12
3694	BriCor_3	physical	28.4893882	-16.3293459	\N	\N	12
3697	Optimus_5	physical	41.7241378	2.9268577	\N	\N	12
3700	Anidia_1	physical	28.1579786	-15.4209285	\N	\N	12
3701	La Estación_1	physical	40.033105	-6.0801056	\N	\N	12
3708	Ferretería Encarna_1	physical	37.6107811	-2.9319037	Calle Puerta Real, 27, 18813, Cuevas del Campo	\N	12
3709	Ferreteria_7	physical	28.0528926	-16.709889	\N	\N	12
3710	Cadena 88_2	physical	37.2109478	-3.6218337	Calle de Luis Buñuel, 6, 18197, Pulianas	https://www.cadena88.com	12
3711	Panizo_1	physical	43.295072	-2.9862907	\N	\N	12
3712	Ferretería Méndez_1	physical	36.9994884	-1.8950881	\N	\N	12
3715	La Llave_4	physical	43.3705837	-8.4029183	\N	\N	12
3716	Rigau_2	physical	41.9618659	2.8043046	Carretera de Santa Coloma, 82	\N	12
3722	La Llave_5	physical	43.2514395	-2.947781	Camilo Villabaso kalea / Calle Camilo Villabaso	\N	12
3728	El Clau Torrent_1	physical	39.4274129	-0.4770742	Carrer del Pare Méndez, 168, 46900, Torrent	\N	12
3729	BricoCentro_1	physical	42.0069853	-4.520064	\N	\N	12
3730	Ferreteria Candau_1	physical	41.5390289	2.4332054	Ronda de Leopold O'Donell, 55, 08302, Mataró	https://www.ferreteriacandau.com/	12
3734	González_2	physical	43.3604428	-8.4098928	\N	http://www.gonzalezferreteria.com/	12
3735	Würth_4	physical	39.6109291	2.6643567	\N	\N	12
3736	Hilti_1	physical	39.609224	2.6616844	\N	\N	12
3737	La Ferretería_3	physical	42.8448094	-2.6843441	Abendaño, 21	\N	12
3738	Ferreteria_8	physical	42.4757187	-7.9860226	\N	\N	12
3739	Würth_5	physical	40.6282809	-4.0184336	\N	\N	12
3742	Ferretería Avenida_3	physical	38.5376161	-0.1186646	Calle de Gerona, Benidorm	\N	12
3743	Ferrobox_1	physical	43.216397	-3.8069154	\N	\N	12
3744	BigMat_3	physical	42.8561422	-4.498801	\N	\N	12
3745	Leroy Merlin_23	physical	37.2848434	-5.9392315	\N	\N	12
3746	La Ferretería_4	physical	38.5388781	-0.1085893	Avinguda de Juan Fuster Zaragoza, 10, 03503, Benidorm	\N	12
3747	Ferretería Avenida_4	physical	41.4031215	-4.3094926	Avenida de la Plaza de Toros, 5, 40200, Cuéllar	\N	12
3748	Sánchez_1	physical	43.1524429	-8.3806087	\N	\N	12
3750	Leroy Merlin_24	physical	37.7901047	-3.7731709	Carretera de Bailén a Motril, Jaén	https://www.leroymerlin.es/tiendas/jaen	12
3751	Montaña_1	physical	43.280215	-2.9833768	Calle Vista Alegre kalea	\N	12
3752	Ferretería Vulcano_1	physical	36.7215936	-4.4307864	Calle Mármoles, 60	\N	12
3753	Sánchez_2	physical	36.3389997	-6.0932161	\N	\N	12
3755	BigMat_4	physical	40.5533655	-4.0212735	\N	\N	12
3756	Ferretería_14	physical	40.6250961	-4.0240145	\N	\N	12
3757	Bricofer_1	physical	38.54521	-0.1330262	Avinguda de Beniardà, Benidorm	\N	12
3763	Prodesco_1	physical	39.4903153	-0.4672548	Calle de la Aviación, 44, 46940	https://prodesco.es/	12
3764	BigMat_5	physical	41.5209757	0.8656455	\N	\N	12
3765	Ferretería Jiménez_1	physical	39.2093108	-1.7247994	\N	\N	12
3766	Garau_1	physical	39.7049203	3.1061588	\N	\N	12
3767	Torres_2	physical	28.1617695	-14.2303352	\N	\N	12
3771	Cadena 88_4	physical	37.1655667	-3.5941607	Calle Poeta Manuel de Góngora, 17	https://www.cadena88.com/es/store/fernando	12
3772	Ferrecal_1	physical	43.3550632	-8.4254247	Rúa Juan de la Cierva, 11, A Coruña	https://ferrecal.com	12
3773	Ferretería Avenida_5	physical	38.0219097	-1.2373302	Avenida de los Pulpites, 2, 30565, Las Torres de Cotillas	https://www.cadena88.com/es	12
3774	Ferretería_15	physical	37.2865047	-5.9114049	\N	\N	12
3775	Ferretería_16	physical	40.3890772	-3.7613946	\N	\N	12
3776	Ferretería Plaza_1	physical	41.6498388	-4.7140974	\N	\N	12
3777	Obramat_2	physical	41.5633922	2.0361425	Avinguda del Vallès, 484-490, 08227, Terrassa	https://www.obramat.es/nuestros-almacenes/bm-terrassa.html	12
3779	Würth_7	physical	39.7123743	2.9025281	\N	\N	12
3780	Obramat_3	physical	41.6148864	0.6569182	Carrer d'Ivars d'Urgell, 25190, Lleida	https://www.bricomart.es/nuestros-almacenes/bm-lleida.html	12
3781	Ferreteria Sant Pau_1	physical	41.6021548	2.6246716	\N	\N	12
3782	Can Manxa_1	physical	42.1812984	2.4877983	\N	\N	12
3794	Cadena 88_5	physical	37.9912631	-1.1253222	\N	\N	12
3798	Leroy Merlin_28	physical	37.8224765	-0.8088524	\N	\N	12
3799	Roma_1	physical	38.9187749	-6.3437068	\N	\N	12
3800	Soto_1	physical	41.3762947	2.1212037	\N	\N	12
3803	Suministros Industriales_1	physical	40.5418143	-3.6263094	\N	\N	12
3808	Ferretería Fernández_2	physical	36.5312611	-6.1885225	\N	\N	12
3809	Optimus_6	physical	28.4693161	-16.2597351	\N	\N	12
3810	Obramat_4	physical	41.1148522	1.225987	Carretera Vella de Valencia, 6 A, Polígon industrial Francoli, 43006, Tarragona	https://www.bricomart.es/nuestros-almacenes/bm-tarragona.html	12
3811	Soto_2	physical	40.752994	-3.784525	\N	\N	12
3812	Suministros Revuelta_1	physical	43.3938152	-3.4612395	\N	\N	12
3814	Marlo_1	physical	28.3567746	-16.3699903	\N	\N	12
3815	BigMat_7	physical	43.2839297	-4.0753863	\N	\N	12
3816	BigMat_8	physical	42.561013	-0.5709669	\N	\N	12
3817	Fontasa_1	physical	41.6782789	-0.9585008	Calle Zuera, 10	\N	12
3819	Ferretería Arenal_3	physical	39.3897141	-3.2108074	\N	\N	12
3820	Ferretería Ruiz_2	physical	38.8901698	-6.6976508	\N	\N	12
3821	Ferretería García_1	physical	38.8919311	-6.6998056	\N	\N	12
3828	Ferretería Vázquez_1	physical	37.5848311	-5.9697207	Calle Vereda de los Rodeos, 51	\N	12
3832	Ferrecal_2	physical	42.8719796	-8.5443324	Avenida de Lugo, 5, 15703, Santiago de Compostela	https://ferrecal.com	12
3833	Optimus_9	physical	41.4303874	2.1786185	\N	\N	12
3834	Leroy Merlin_31	physical	40.6592558	-3.7560059	\N	\N	12
3836	Ferretería Venecia_3	physical	40.4223	-3.7106539	\N	\N	12
3837	BricoCentro_2	physical	40.9206149	-4.1130448	\N	\N	12
3844	Vidal bobinatjes de motors i bombes_1	physical	41.1456479	1.1065389	Carrer de Benidorm, 30 LOCAL, 43205, Reus	\N	12
3845	Ferreteria_12	physical	28.1537909	-17.1991179	\N	\N	12
3849	Ferreteria Montseny_1	physical	41.294808	1.256116	Carretera del Pla, 100, 43800, Valls	\N	12
3850	Ferretería Martínez_1	physical	42.8311758	-1.6362137	\N	\N	12
3851	Ferreteria Martí_1	physical	40.7176649	0.7325691	\N	\N	12
3852	Obramat_6	physical	39.4127447	-0.3882817	\N	https://www.bricomart.es	12
3689	Ferretería Luna_1	physical	38.3542826	-2.8032813	\N	\N	12
3690	Ferretería_12	physical	40.2931102	-3.8224501	\N	\N	12
3691	Ferreteria Barral_1	physical	42.1038202	-8.5609735	\N	\N	12
3695	Ferrokey_1	physical	38.3975005	-0.4366254	\N	\N	12
3696	BriCor_4	physical	40.4297058	-3.7168497	\N	\N	12
3698	Ferretería Sánchez_5	physical	37.2260107	-3.6851555	Calle Cedazos, 61, 18230, Atarfe	http://ferreteria-sanchez.es/es	12
3699	Bricordino_1	physical	28.1487707	-15.4285147	\N	\N	12
3702	La Plataforma de la Construcción_1	physical	40.4047072	-3.6984734	\N	\N	12
3703	La Chispa_1	physical	41.4093775	2.1887425	\N	\N	12
3704	Ferretería Venecia_1	physical	40.4465209	-3.710967	\N	\N	12
3705	Ferretería Santa Clotilde_1	physical	37.2230572	-3.6408973	Calle Alquife, 18220, Albolote	https://santaclotilde.es/	12
3706	Ferretería Venecia_2	physical	40.4396955	-3.7126581	\N	\N	12
3707	Ferrokey_2	physical	40.3558628	-3.9021379	Avenida del Príncipe de Asturias, 127, 28670, Villaviciosa de Odón	\N	12
3713	La Llave_3	physical	42.0045113	-4.5239362	\N	\N	12
3714	Bauhaus_1	physical	41.9660933	2.7807874	\N	\N	12
3717	Ferrokey_3	physical	38.9790477	-0.6890134	\N	\N	12
3718	Cadena 88_3	physical	41.3679535	2.0185111	Avinguda Santa Coloma, 20, 08690, Santa Coloma de Cervelló	\N	12
3719	Leroy Merlin_19	physical	36.53567	-4.6361662	\N	\N	12
3720	Ferretería Plácido_1	physical	36.7833241	-4.1067867	Calle Reñidero, 16, Vélez-Málaga	\N	12
3721	Ferretería San José_2	physical	40.5748233	-4.0037679	\N	\N	12
3723	Elma_1	physical	40.3532763	-3.5449364	\N	http://www.sumelma.distribuidor-oficial.es	12
3724	Leroy Merlin_20	physical	41.6023084	2.2591146	\N	\N	12
3725	Leroy Merlin_21	physical	41.6033068	2.2597071	\N	\N	12
3726	Leroy Merlin_22	physical	43.1644399	-2.6196967	\N	\N	12
3727	Brico_1	physical	42.3484724	-3.7138275	\N	\N	12
3731	Palerm_1	physical	39.5280653	2.5059713	\N	\N	12
3732	Ferretería Ortiz_1	physical	40.4040552	-3.6551043	Calle de la Cerámica, 88, 28038, Madrid	https://ferreteriaortiz.es	12
3733	Ferretería_13	physical	40.622308	-3.9055699	\N	\N	12
3740	Ferretería Arenal_2	physical	39.4055086	-3.1224883	\N	\N	12
3741	Ferretería Bisal_1	physical	42.0890413	-8.4191123	Rúa Entrecines	\N	12
3749	Ferretería Roberto_1	physical	41.6627689	-4.7224946	\N	\N	12
3754	Ferretería La Llave_1	physical	43.2175994	-6.8766338	\N	\N	12
3758	Ferretería Los Pinos_1	physical	38.5380934	-0.1237446	Carrer de Girona - Calle de Gerona, Benidorm	\N	12
3759	Ferretería El Carmen_1	physical	39.2761635	-0.2756296	\N	https://www.cadena88.com/es	12
3760	Can Xic_1	physical	39.6177668	2.771023	\N	\N	12
3761	Cano_1	physical	39.5595489	2.898461	\N	\N	12
3762	Leroy Merlin_25	physical	41.3876338	2.1722409	Carrer de Fontanella, 12	https://leroymerlin.es	12
3768	Obramat_1	physical	38.5349221	-0.1813141	\N	https://www.bricomart.es	12
3769	Fuente el Sol_1	physical	41.6626411	-4.7355853	\N	\N	12
3770	Würth_6	physical	28.0950848	-17.1139272	\N	\N	12
3778	Ferrokey_4	physical	40.4586859	-3.7833706	Plaza del Marqués de Camarines	\N	12
3783	Ferreteria Puig_1	physical	42.1826555	2.4903807	\N	\N	12
3784	Ferreteria La Clau_1	physical	39.0778663	-0.5112467	\N	\N	12
3785	BriCor_5	physical	43.3664082	-5.8495033	Calle General Elorza, 75, 33002, Oviedo / Uviéu	\N	12
3786	Leroy Merlin_26	physical	41.2272629	1.7406955	Ronda d'Europa, 46	\N	12
3787	Leroy Merlin_27	physical	41.2272266	1.7407143	Ronda d'Europa, 46	\N	12
3788	Ferretería Ruiz_1	physical	36.7040591	-3.4886375	\N	https://www.ferreteriaruiz.com/	12
3789	El Martillo_2	physical	38.0937643	-1.7836981	Ronda Este, 30430, Cehegín	\N	12
3790	Brico Centro_1	physical	40.410216	0.3969713	\N	\N	12
3791	Brico Dépôt_2	physical	41.6271697	0.6096574	Avinguda de l'Alcalde Rovira Roure, 108,110, 25198, Lleida	http://www.bricodepot.es/	12
3792	ferrCASH_1	physical	40.363985	-3.5970788	\N	\N	12
3793	Ferretería Bazar_1	physical	42.8798507	-8.5334477	Costa do Vedor, Santiago de Compostela	\N	12
3795	Ferreteria_9	physical	41.3540676	2.1132732	Avinguda d'Europa, 95, 08907, L'Hospitalet de Llobregat	\N	12
3796	Ferreteria Marina_1	physical	41.3532621	2.1135321	Avinguda d'Europa, 23, 08907, L'Hospitalet de Llobregat	\N	12
3797	Ferreteria_10	physical	27.772268	-15.6057207	\N	\N	12
3801	Ferrobox_2	physical	28.6566245	-17.908481	\N	\N	12
3802	Ferretería Casado_1	physical	43.4532383	-3.7431262	\N	\N	12
3804	BigMat Femalsa_1	physical	41.0543349	-4.7106683	\N	\N	12
3805	Centro_1	physical	42.518237	-0.3649043	\N	\N	12
3806	BigMat_6	physical	36.3692404	-5.2304875	\N	\N	12
3807	Ferreteria Optimus_1	physical	41.4148718	2.1649787	Avinguda de la Mare de Déu de Montserrat, 73, 08024, Barcelona	\N	12
3813	Ferretería Cabrales_1	physical	36.3459839	-5.8160551	\N	\N	12
3818	La Ferretería_5	physical	40.0600146	-5.7536819	\N	\N	12
3822	Optimus_7	physical	41.4000531	2.1550527	\N	\N	12
3823	Optimus_8	physical	41.401979	2.1532149	\N	\N	12
3824	Husqvarna_1	physical	39.4856106	2.8922516	\N	\N	12
3825	Leroy Merlin_29	physical	43.3641383	-5.8487443	Calle Posada Herrera, Oviedo / Uviéu	\N	12
3826	Leroy Merlin_30	physical	37.6376843	-1.6986887	\N	\N	12
3827	Burgalesa_1	physical	42.34849	-3.6965061	\N	\N	12
3829	Ferrymas_3	physical	41.6316292	-0.8866408	\N	\N	12
3830	Ferreteria_11	physical	27.7572189	-15.6814653	Arguineguin	\N	12
3831	Ferretería González_1	physical	37.1437171	-1.8272849	Paseo del Mediterráneo, 411, 04638, Mojácar Playa	\N	12
3835	Obramat_5	physical	41.3484927	2.1158798	Carrer de les Ciències, 140, 08908, L'Hospitalet de Llobregat	\N	12
3838	Ferretería Vidal_2	physical	42.2811649	-8.6097508	Rúa José Regojo, 17, 36800, Redondela	https://ferreteriavidal.es	12
3839	Ferretería Guanarteme_1	physical	28.097388	-15.4424267	Luis Saavedra Miranda, 4, 35014, Las Palmas de Gran Canaria	\N	12
3840	Ferretería La Llave_2	physical	36.7205013	-4.3548885	Calle Almería, 75, 29017	\N	12
3841	Leroy Merlin_32	physical	38.9742257	-3.9167426	\N	\N	12
3842	Sol_1	physical	37.1764614	-3.6076585	Calle Pintor López Mezquita, 9, 18002, Granada	https://www.cerrajeriasol.es	12
3843	González_3	physical	40.1241652	-5.7008248	\N	\N	12
3846	Ferretería La Llave_3	physical	36.7210526	-4.4098203	Paseo de Reding, 31, 29016	\N	12
3847	FSáenz_1	physical	36.7338477	-4.4169802	Calle Zurbarán, 23	https://www.fsaenz.com/	12
3848	Ferrymas_4	physical	39.2820062	-0.4255495	Avinguda de les Germanies, 27, 46450, Benifaió	\N	12
3856	Cadena 88_6	physical	28.0522197	-16.7151422	\N	\N	12
4010	Bricomat_2	physical	\N	\N	\N	\N	12
3853	Taller Salvat_1	physical	40.6854586	0.5825034	Carrer del Loira, 36, 43870, Amposta	https://www.tallersalvat.com/	12
3854	Würth_8	physical	40.456739	0.4494911	\N	\N	12
3855	Würth_9	physical	38.5323013	-0.1670309	\N	\N	12
3857	Würth_10	physical	36.7370147	-3.5127286	\N	\N	12
3858	La Muralla_1	physical	40.3477113	-3.8090861	Avenida de la Libertad, 28924, Alcorcón	\N	12
3859	Cadena 88_7	physical	37.3021194	-6.2976591	\N	\N	12
3864	La Ferreteria_1	physical	39.1701294	-3.0213482	Carretera de Argamasilla de Alba	\N	12
3904	Leroy Merlin_50	physical	\N	\N	\N	\N	12
3905	Leroy Merlin_51	physical	\N	\N	\N	\N	12
3906	Leroy Merlin_52	physical	\N	\N	Rúa de Polonia, 1, 15707, Santiago de Compostela	\N	12
3907	Brico Dépôt_4	physical	\N	\N	\N	\N	12
3908	Leroy Merlin_53	physical	\N	\N	Avenida La Ribera, 48903, Barakaldo	\N	12
3909	Bauhaus_6	physical	\N	\N	\N	\N	12
3910	Leroy Merlin_54	physical	\N	\N	\N	\N	12
3911	Leroy Merlin_55	physical	\N	\N	\N	https://www.leroymerlin.es/tiendas/aldaia	12
3912	Leroy Merlin_56	physical	\N	\N	08349, Cabrera de Mar	\N	12
3913	Leroy Merlin_57	physical	\N	\N	\N	https://www.leroymerlin.es/tiendas/compact-ferrol	12
3914	Brico Dépôt_5	physical	\N	\N	\N	\N	12
3915	Leroy Merlin_58	physical	\N	\N	\N	https://www.leroymerlin.es/	12
3916	Leroy Merlin_59	physical	\N	\N	\N	\N	12
3917	Brico Dépôt_6	physical	\N	\N	\N	https://www.bricodepot.es/	12
3918	Leroy Merlin_60	physical	\N	\N	\N	\N	12
3919	Leroy Merlin_61	physical	\N	\N	Carretera Majadahonda a Boadilla, 28222, Majadahonda	https://www.leroymerlin.es/tiendas/majadahonda.html	12
3920	Leroy Merlin_62	physical	\N	\N	\N	\N	12
3922	Leroy Merlin_64	physical	\N	\N	\N	\N	12
3927	BdB Esteso_1	physical	\N	\N	\N	\N	12
3928	Leroy Merlin_68	physical	\N	\N	Camino Loma de San Julián	\N	12
3943	Ferreteria_15	physical	\N	\N	22430, Graus	\N	12
3944	Saneamientos Pereda_1	physical	\N	\N	\N	\N	12
3945	Brico Dépôt_11	physical	\N	\N	Rúa Severo Ochoa, 21, 15008, A Coruña	https://www.bricodepot.es/	12
3946	Leroy Merlin_72	physical	\N	\N	\N	\N	12
3951	Leroy Merlin_74	physical	\N	\N	\N	\N	12
3952	Ferreteria Los Manantiales_1	physical	\N	\N	\N	\N	12
3953	Es Brico_1	physical	\N	\N	\N	\N	12
3954	Brico Dépôt_13	physical	\N	\N	El Pedréu, 33468, Tresona	\N	12
3955	Brico Dépôt_14	physical	\N	\N	\N	\N	12
3956	Brico Dépôt_15	physical	\N	\N	\N	\N	12
3957	Bauhaus_9	physical	\N	\N	\N	\N	12
3958	Comercial Metabos_2	physical	\N	\N	Avenida de Carbajosa, 7, 37188, Carbajosa de la Sagrada	http://www.metabos.com	12
3959	Leroy Merlin_75	physical	\N	\N	Carrertera de Rubí, 7, 08174, Sant Cugat del Vallès	\N	12
3960	Leroy Merlin_76	physical	\N	\N	Calle de Laguardia, 4, 28022, Madrid	\N	12
3968	Leroy Merlin_80	physical	\N	\N	\N	\N	12
3969	Leroy Merlin_81	physical	\N	\N	\N	\N	12
3970	Leroy Merlin_82	physical	\N	\N	\N	\N	12
3971	Leroy Merlin_83	physical	\N	\N	Carretera de Palma del Río	https://www.leroymerlin.es	12
3972	Würth_12	physical	\N	\N	\N	\N	12
3973	Obramat_13	physical	\N	\N	\N	https://www.bricomart.es	12
3974	Leroy Merlin_84	physical	\N	\N	Badajoz	\N	12
3993	Leroy Merlin_89	physical	\N	\N	Barrio Peruri, 33, 48940, Leioa - Lejona	https://www.leroymerlin.es/	12
3994	Leroy Merlin_90	physical	\N	\N	Puerto Real	\N	12
3999	Leroy Merlin_93	physical	\N	\N	\N	\N	12
4000	Leroy Merlin_94	physical	\N	\N	\N	\N	12
4001	Ferretería Martín_1	physical	\N	\N	\N	\N	12
4002	Bauhaus_11	physical	\N	\N	Calle Sector 1 Ab, 2F, 46910	\N	12
4003	Leroy Merlin_95	physical	\N	\N	\N	\N	12
4004	Leroy Merlin Compact_1	physical	\N	\N	\N	\N	12
4006	BriCor_6	physical	\N	\N	\N	\N	12
4007	Aguilar_1	physical	\N	\N	Avenida do Marqués de Figueroa, 102-104, 15500, Fene	\N	12
4021	Leroy Merlin_103	physical	\N	\N	Avenida de la Constitución, 102, 28850, Torrejón de Ardoz	https://www.leroymerlin.es/tiendas/compact-torrejon.html	12
4022	Würth_14	physical	\N	\N	Carrer de la Múnia, 36, 08720, Vilafranca del Penedès	https://www.wurth.es	12
4023	Hilti_2	physical	\N	\N	Carretera de Villaverde a Vallecas, 259	\N	12
4024	Obramat_20	physical	\N	\N	Avinguda del Conflent, 08915, Badalona	\N	12
4027	Leroy Merlin_104	physical	\N	\N	\N	\N	12
4028	Leroy Merlin_105	physical	\N	\N	\N	\N	12
4029	Obramat_21	physical	\N	\N	\N	https://www.bricomart.es	12
4030	Leroy Merlin_106	physical	\N	\N	Avinguda de la Generalitat, Tortosa	\N	12
4031	Obramat_22	physical	\N	\N	\N	https://www.bricomart.es	12
4032	Obramat_23	physical	\N	\N	\N	https://www.bricomart.es	12
4033	Electro Molina_1	physical	\N	\N	Avinguda Puigdomí	\N	12
4039	BigMat_13	physical	\N	\N	\N	\N	12
4057	Bauhaus_13	physical	\N	\N	\N	\N	12
4058	Leroy Merlin_117	physical	\N	\N	\N	\N	12
4059	Bauhaus_14	physical	\N	\N	Carrer de Cartagena, 11, 17005, Girona	\N	12
4060	Leroy Merlin_118	physical	\N	\N	\N	\N	12
4061	Leroy Merlin_119	physical	\N	\N	\N	\N	12
4062	Leroy Merlin_120	physical	\N	\N	Camino de la Paloma, 25, 30150, La Alberca	https://www.leroymerlin.es/	12
3860	Obramat_7	physical	41.2378362	1.7300189	Carrer de l'Acer, 13, 08800, Vilanova i la Geltrú	https://www.obramat.es/nuestros-almacenes/bm-vilanova.html	12
3861	Obramat_8	physical	41.5179043	2.1001599	Carrer de la Serra de Galliners, 24, 08205, Sabadell	\N	12
3862	Aldana_1	physical	43.3067417	-2.3879693	\N	\N	12
3863	BricoCentro_3	physical	39.1727672	-3.0220181	Camino de Alcázar, 36	https://www.bricocentrotomelloso.es/	12
3865	Merino_1	physical	40.3544206	-3.6868205	\N	\N	12
3866	Rucho_1	physical	42.8548672	-7.1634018	\N	\N	12
3867	La Muralla_2	physical	37.8933983	-4.7700907	\N	\N	12
3868	Ferreteria_13	physical	40.3976736	-3.7701009	\N	\N	12
3869	Cadena 88_8	physical	40.3984831	-3.7743536	\N	\N	12
3870	Ferretería García_2	physical	42.7855787	-8.8842162	Corredoira de Luís Cadarso Rey	\N	12
3871	Ferretería Plaza_2	physical	41.6507449	-4.7127506	\N	\N	12
3872	Ferretería Chamartín_1	physical	40.4645321	-3.6945843	\N	\N	12
3873	Ferretería La Purísima_1	physical	38.5000804	-5.1448133	Calle Mercado, 7, 14270, Hinojosa del Duque	\N	12
3874	Ferretería Garsan_1	physical	43.5381442	-5.6938356	Calle Los Andes, 6	\N	12
3875	Ferretería El Puente_1	physical	28.685003	-17.7658981	\N	\N	12
3876	Ferreteria_14	physical	40.403889	-3.7143534	Paseo de Juan Antonio Vallejo-Nájera Botas, 48	\N	12
3877	Leroy Merlin_33	physical	\N	\N	\N	\N	12
3878	Leroy Merlin_34	physical	\N	\N	\N	\N	12
3879	Leroy Merlin_35	physical	\N	\N	\N	\N	12
3880	Leroy Merlin_36	physical	\N	\N	Avinguda de la Marina, 17	https://www.leroymerlin.es/	12
3881	Leroy Merlin_37	physical	\N	\N	\N	\N	12
3882	Leroy Merlin_38	physical	\N	\N	\N	\N	12
3883	An de Juan_1	physical	\N	\N	Carretera de Galapagar a Villalba, km. 1	http://www.ajcenter.es/	12
3884	Obramat_9	physical	\N	\N	Avenida de los Rosales, 24	https://www.obramat.es/	12
3885	Leroy Merlin_39	physical	\N	\N	Alcalá de Henares	\N	12
3886	Leroy Merlin_40	physical	\N	\N	46120, Alboraia	https://www.leroymerlin.es/tiendas/alboraya.html	12
3887	Leroy Merlin_41	physical	\N	\N	\N	\N	12
3888	Leroy Merlin_42	physical	\N	\N	\N	\N	12
3889	Leroy Merlin_43	physical	\N	\N	Alcorcón	\N	12
3890	Bricocentro_1	physical	\N	\N	\N	\N	12
3891	BricoCentro_4	physical	\N	\N	\N	\N	12
3892	Brico Dépôt_3	physical	\N	\N	Alcalá de Henares	\N	12
3893	Leroy Merlin_44	physical	\N	\N	\N	\N	12
3894	Bauhaus_2	physical	\N	\N	Carrer Victoria Gasteiz, 17003, Girona	https://www.bauhaus.es/	12
3895	Leroy Merlin_45	physical	\N	\N	\N	\N	12
3896	Bauhaus_3	physical	\N	\N	\N	\N	12
3897	Leroy Merlin_46	physical	\N	\N	Carrer de Josep Maria Folch i Torres, 43120, Tarragona	\N	12
3898	Leroy Merlin_47	physical	\N	\N	\N	\N	12
3899	Bauhaus_4	physical	\N	\N	Calle Palencia, 3, 29004, Málaga	https://www.bauhaus.es/	12
3900	Leroy Merlin_48	physical	\N	\N	\N	\N	12
3901	Leroy Merlin_49	physical	\N	\N	\N	\N	12
3902	Bauhaus_5	physical	\N	\N	Calle de Campezo, 12, 28022, Madrid	https://www.bauhaus.es/	12
3903	Ferrobox_3	physical	\N	\N	\N	\N	12
3921	Leroy Merlin_63	physical	\N	\N	\N	\N	12
3923	Leroy Merlin_65	physical	\N	\N	\N	\N	12
3924	Leroy Merlin_66	physical	\N	\N	Calle Me Falta un Tornillo, 3, 47195, Arroyo de la Encomienda	\N	12
3925	Leroy Merlin_67	physical	\N	\N	12A	\N	12
3926	Brico Dépôt_7	physical	\N	\N	carrer La Bassa, 08150, Parets del Vallès	\N	12
3929	BigMat_9	physical	\N	\N	\N	\N	12
3930	Leroy Merlin_69	physical	\N	\N	Carrer de Dinamarca, 4, 08917	\N	12
3931	Aki_2	physical	\N	\N	\N	https://www.leroymerlin.es/aki-leroy-merlin	12
3932	BigMat_10	physical	\N	\N	\N	\N	12
3933	Brico Dépôt_8	physical	\N	\N	\N	\N	12
3934	Leroy Merlin Alcalá de Guadaíra_1	physical	\N	\N	Alcalá de Guadaíra	\N	12
3935	Leroy Merlin_70	physical	\N	\N	Carrer Medi Ambient, 1, 46470	\N	12
3936	Brico Dépôt_9	physical	\N	\N	\N	\N	12
3937	Leroy Merlin_71	physical	\N	\N	\N	\N	12
3938	Bauhaus_7	physical	\N	\N	\N	https://www.bauhaus.es	12
3939	Brico Dépôt_10	physical	\N	\N	\N	\N	12
3940	Obramat_10	physical	\N	\N	\N	https://www.bricomart.es	12
3941	Obramat_11	physical	\N	\N	\N	https://www.bricomart.es	12
3942	Würth_11	physical	\N	\N	\N	\N	12
3947	Leroy Merlin_73	physical	\N	\N	\N	\N	12
3948	Bauhaus_8	physical	\N	\N	\N	\N	12
3949	Brico Dépôt_12	physical	\N	\N	\N	\N	12
3950	Bricopinares_1	physical	\N	\N	Calle la Dehesa, 3, 09670	\N	12
3961	BricoCentro_5	physical	\N	\N	Carretera de Valladolid, 33, 37184, Villares de la Reina	http://www.bricoaguilar.es/	12
3962	Brico Dépôt_16	physical	\N	\N	\N	\N	12
3963	Es Brico_2	physical	\N	\N	\N	\N	12
3964	Obramat_12	physical	\N	\N	\N	https://www.bricomart.es	12
3965	Leroy Merlin_77	physical	\N	\N	Calle de Trafalgar, 19004, Guadalajara	https://www.leroymerlin.es/tiendas/compact-guadalajara	12
3966	Leroy Merlin_78	physical	\N	\N	\N	\N	12
3967	Leroy Merlin_79	physical	\N	\N	\N	\N	12
3975	Brico Dépôt_17	physical	\N	\N	\N	\N	12
3976	Ferretería Ortiz_2	physical	\N	\N	\N	\N	12
3977	La Herramienta Balear_1	physical	\N	\N	\N	\N	12
3978	Obramat_14	physical	\N	\N	\N	\N	12
3979	Porcelanosa_1	physical	\N	\N	Avenida de Parayas, 48, 39011, Santander	https://www.porcelanosa.com/	12
3980	Sánchez_3	physical	\N	\N	\N	\N	12
3981	Canaima_1	physical	\N	\N	Camiño Basanta	http://www.canaima.es/	12
3982	Leroy Merlin_85	physical	\N	\N	\N	\N	12
3983	Brico Dépôt_18	physical	\N	\N	\N	\N	12
3984	Leroy Merlin_86	physical	\N	\N	Avenida San Rafael, 18006, Armilla	\N	12
3985	Bricomat_1	physical	\N	\N	Calle Estocolmo, 1, 42110, Ólvega	\N	12
3986	Brico Dépôt_19	physical	\N	\N	Avinguda de la Llibertat, 1, 46600, Alzira	https://www.bricodepot.es/tiendas/brico-depot-alzira	12
3987	BricoCentro_6	physical	\N	\N	\N	https://www.bricocentroaranda.es/	12
3988	Leroy Merlin_87	physical	\N	\N	\N	https://www.leroymerlin.es/	12
3989	Leroy Merlin_88	physical	\N	\N	Palmones	\N	12
3990	Würth_13	physical	\N	\N	\N	\N	12
3991	Ferretería La Llave_4	physical	\N	\N	Avenida de Mugardos, 6, 15624, Ares	\N	12
3992	Obramat_15	physical	\N	\N	\N	https://www.bricomart.es	12
3995	Obramat_16	physical	\N	\N	Calle Armada Española, 28922, Alcorcón	https://www.bricomart.es	12
3996	Bauhaus_10	physical	\N	\N	Calle Ejército del Aire, 28922, Alcorcón	https://www.bauhaus.es/es/nuestros-centros	12
3997	Leroy Merlin_91	physical	\N	\N	Carrer de Maria Callas, 2, 43883, Roda de Berà	\N	12
3998	Leroy Merlin_92	physical	\N	\N	\N	\N	12
4005	Ferretería SAR_1	physical	\N	\N	\N	\N	12
4008	Leroy Merlin_96	physical	\N	\N	\N	\N	12
4009	Leroy Merlin_97	physical	\N	\N	Camí dels Rolls, 46500, Sagunto	\N	12
4011	Obramat_17	physical	\N	\N	Avenida Manuel Castillo, 29004	https://www.bricomart.es/nuestros-almacenes/bm-malaga.html	12
4012	Obramat_18	physical	\N	\N	\N	https://www.bricomart.es	12
4013	Brico Dépôt_20	physical	\N	\N	Carrer Satsuma, 1, 12539, les Alqueries / Alquerías del Niño Perdido	\N	12
4014	Leroy Merlin_98	physical	\N	\N	Carretera de Madrid, 114, 45600, Talavera de la Reina	\N	12
4015	Bauhaus_12	physical	\N	\N	\N	\N	12
4016	Leroy Merlin_99	physical	\N	\N	\N	\N	12
4017	Leroy Merlin_100	physical	\N	\N	Lintzirin Poligonoa, 12, 20180, Oiartzun	\N	12
4018	Obramat_19	physical	\N	\N	Avenida de Galicia, Carbajosa de la Sagrada	https://www.bricomart.es	12
4019	Leroy Merlin_101	physical	\N	\N	\N	\N	12
4020	Leroy Merlin_102	physical	\N	\N	Carrer d'Astúries, 66, 17003, Girona	\N	12
4025	BigMat_11	physical	\N	\N	\N	\N	12
4026	Roycha_3	physical	\N	\N	Calle Valle de Manzanedo, 1	\N	12
4034	Leroy Merlin_107	physical	\N	\N	\N	\N	12
4035	Obramat_24	physical	\N	\N	Calle La Flauta Mágica, 25, 28222, Majadahonda	https://www.obramat.es/	12
4036	Leroy Merlin_108	physical	\N	\N	\N	\N	12
4037	BigMat_12	physical	\N	\N	\N	\N	12
4038	Habitacle_1	physical	\N	\N	Carretera d'Artà, 89, 07458	http://habitaclemallorca.com	12
4040	Leroy Merlin_109	physical	\N	\N	\N	\N	12
4041	Leroy Merlin_110	physical	\N	\N	\N	\N	12
4042	Fesmés_1	physical	\N	\N	Carrer del Pallars, 2, 08812	\N	12
4043	Leroy Merlin_111	physical	\N	\N	\N	\N	12
4044	Saltoki_1	physical	\N	\N	\N	\N	12
4045	Leroy Merlin_112	physical	\N	\N	\N	\N	12
4046	Consydecor_1	physical	\N	\N	Carretera de Aspe a Los Hondones, 03680, Aspe	https://consydecor.com/	12
4047	Obramat_25	physical	\N	\N	Rúa Durán Loriga Juan Jacobo (matemático), 10, 27003, Lugo	https://www.bricomart.es	12
4048	BigMat_14	physical	\N	\N	\N	\N	12
4049	Ferreteria Martí_2	physical	\N	\N	Carrer de la Tolerància, 16, Reus	\N	12
4050	BigMat_15	physical	\N	\N	\N	\N	12
4051	Torsesa_1	physical	\N	\N	\N	\N	12
4052	Leroy Merlin_113	physical	\N	\N	\N	\N	12
4053	Leroy Merlin_114	physical	\N	\N	\N	https://www.leroymerlin.es/	12
4054	Saltoki_2	physical	\N	\N	\N	\N	12
4055	Leroy Merlin_115	physical	\N	\N	\N	\N	12
4056	Leroy Merlin_116	physical	\N	\N	\N	\N	12
4063	Leroy Merlin	chain	\N	\N	\N	\N	\N
4064	BRICO DEPOT	chain	\N	\N	\N	\N	\N
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.tags (id, name) FROM stdin;
1	mock-data
\.


--
-- Data for Name: user_tags; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.user_tags (user_id, tag_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: partle_user
--

COPY public.users (id, email, password_hash) FROM stdin;
1	demo@partle.dev	$2b$12$jyztUAFohj8XD80DbjAhTerTlXm5lUs4b14RRJC9BB/YP6F06lGY.
2	caca@gmail.com	$2b$12$xd4ZNPpi9MD0llPKg8fyGe/O0sT8PfpDBhR.CAIr2rssJhl6KHlo6
4	test@gmail.com	$2b$12$/Qlxv5PG7LHGlcUNqJ3tRO16eZWiYs6iW6y7fSTo4xb72dYSLUd2y
5	pato@gmail.com	$2b$12$2UEdjAwZtziJ.uoM//5J2etuBUcAy54Ex2Xn26AVWXAn9MB2LkhSO
6	patopato@gmail.com	\N
7	patoo@gmail.com	\N
8	test@example.com	$2b$12$f2hzfDYbtn9frK6KywelcOTNIp9YwXo4jU0rYvHwENL391Ufy/KFG
9	a@gmail.com	\N
10	b@gmail.com	$2b$12$VHjYY7l2nxIcMuXMQ5nD6.FfCnkUQoAbLBATXlIjZlCDMTWHTh0Pm
11	c@gmail.com	$2b$12$/oESS8uV3yZzPLfY22xMtOwr2Tg1zEsE6.ao4yjXHqGe5ONEA1b1u
12	ruben.jimenezmejias@gmail.com	$2b$12$ybWqzPKvOJDrC5VfzPsZbeUPVjneJIgbwuVvJn0/Ybqm3gbZm2b9S
14	mockuser@example.com	$2b$12$Gp2IyBCMOcslmcjjW3bS7etXo4axYGfSCGE/BstukgZIBsu7u2mjy
\.


--
-- Name: credentials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: partle_user
--

SELECT pg_catalog.setval('public.credentials_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: partle_user
--

SELECT pg_catalog.setval('public.products_id_seq', 38, true);


--
-- Name: stores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: partle_user
--

SELECT pg_catalog.setval('public.stores_id_seq', 4064, true);


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: partle_user
--

SELECT pg_catalog.setval('public.tags_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: partle_user
--

SELECT pg_catalog.setval('public.users_id_seq', 14, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: credentials credentials_credential_id_key; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.credentials
    ADD CONSTRAINT credentials_credential_id_key UNIQUE (credential_id);


--
-- Name: credentials credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.credentials
    ADD CONSTRAINT credentials_pkey PRIMARY KEY (id);


--
-- Name: product_tags product_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.product_tags
    ADD CONSTRAINT product_tags_pkey PRIMARY KEY (product_id, tag_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: store_tags store_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.store_tags
    ADD CONSTRAINT store_tags_pkey PRIMARY KEY (store_id, tag_id);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: user_tags user_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.user_tags
    ADD CONSTRAINT user_tags_pkey PRIMARY KEY (user_id, tag_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_tags_name; Type: INDEX; Schema: public; Owner: partle_user
--

CREATE UNIQUE INDEX ix_tags_name ON public.tags USING btree (name);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: partle_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: credentials credentials_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.credentials
    ADD CONSTRAINT credentials_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: product_tags product_tags_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.product_tags
    ADD CONSTRAINT product_tags_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: product_tags product_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.product_tags
    ADD CONSTRAINT product_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: products products_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- Name: products products_creator_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_creator_id_fkey1 FOREIGN KEY (creator_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: products products_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE SET NULL;


--
-- Name: products products_updated_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_updated_by_id_fkey FOREIGN KEY (updated_by_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: store_tags store_tags_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.store_tags
    ADD CONSTRAINT store_tags_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id);


--
-- Name: store_tags store_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.store_tags
    ADD CONSTRAINT store_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: stores stores_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: user_tags user_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.user_tags
    ADD CONSTRAINT user_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: user_tags user_tags_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: partle_user
--

ALTER TABLE ONLY public.user_tags
    ADD CONSTRAINT user_tags_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO partle_user;


--
-- PostgreSQL database dump complete
--

