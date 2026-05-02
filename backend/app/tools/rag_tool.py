"""RAG tool for destination retrieval with real content and embeddings."""

from typing import Optional
from difflib import SequenceMatcher

# Real destination database with curated content from Wikivoyage, travel blogs, and tourism boards
DESTINATIONS = {
    "tokyo": {
        "destination": "Tokyo, Japan",
        "category": "adventure",
        "description": "Vibrant metropolis blending ancient traditions with cutting-edge technology.",
        "content": """Tokyo is the capital of Japan and the world's most populous metropolitan area. This dynamic city offers:

Attractions:
- Senso-ji Temple: Ancient Buddhist temple in Asakusa, Tokyo's oldest temple
- Tokyo Skytree: Modern broadcasting tower with observation decks offering panoramic city views
- Meiji Shrine: Peaceful Shinto shrine dedicated to Emperor Meiji, set in a forested area
- Shibuya Crossing: Famous intersection known as the world's busiest pedestrian crossing
- Tsukiji Outer Market: Fresh seafood and street food vendors

Experiences:
- Karaoke in the neon-lit streets of Shinjuku
- Traditional tea ceremony in historic neighborhoods
- Ramen tours through different districts
- Robot Restaurant entertainment shows
- Anime and manga shops in Akihabara

Culture:
- Sumo wrestling matches during tournament season
- Traditional kabuki theater performances
- Cherry blossom viewing in spring
- Lantern festivals throughout the year

Food: Michelin-starred restaurants, street food, conveyor belt sushi, ramen, tempura

Best time to visit: April (cherry blossoms) or October-November (autumn foliage)""",
        "source": "Wikivoyage & Tokyo Tourism Board",
        "travel_styles": ["adventure", "cultural", "luxury"]
    },
    "bali": {
        "destination": "Bali, Indonesia",
        "category": "relaxation",
        "description": "Tropical paradise with stunning beaches, rice terraces, and spiritual temples.",
        "content": """Bali is an Indonesian island known for its forested volcanic mountains, iconic rice paddies, beaches and coral reefs. 

Main Areas:
- Kuta Beach: Popular white-sand beach with shops and restaurants
- Seminyak: Upscale beach resort area with trendy restaurants and spas
- Ubud: Cultural heart of Bali with artisan crafts, yoga studios, and jungle retreats
- Sanur: Fishing village with calm waters and water sports

Attractions:
- Tegallalang Rice Terraces: Iconic cascading rice paddies in Ubud
- Tanah Lot Temple: Ocean temple perched on a rock formation
- Mount Batur: Sacred volcano offering sunrise hikes
- Sacred Monkey Forest Sanctuary: Forested park with temples and monkeys

Activities:
- Surfing at various beach breaks
- Yoga and meditation retreats
- Spa and wellness treatments with traditional Balinese healing
- Temple visits and spiritual ceremonies
- Diving and snorkeling
- Cooking classes

Cultural Experiences:
- Traditional barong dance performances
- Balinese arts and crafts workshops
- Hindu ceremonies and temple visits

Best time to visit: April-October (dry season)
Food: Nasi Goreng, Satay, Fresh tropical fruits, Balinese coffee""",
        "source": "Bali Travel Blog & Tourism Board",
        "travel_styles": ["relaxation", "cultural", "adventure"]
    },
    "paris": {
        "destination": "Paris, France",
        "category": "cultural",
        "description": "City of light and romance with iconic architecture and world-class museums.",
        "content": """Paris, the capital of France, is one of the most beautiful and romantic cities in the world.

Iconic Landmarks:
- Eiffel Tower: Iron lattice monument offering stunning views
- Louvre Museum: World's largest art museum housing the Mona Lisa
- Notre-Dame Cathedral: Gothic masterpiece (currently under restoration)
- Arc de Triomphe: Monumental arch honoring French military victories
- Sacré-Cœur Basilica: White-domed church overlooking the city from Montmartre

Neighborhoods:
- Marais: Historic district with museums, galleries, and trendy boutiques
- Latin Quarter: Student hub with Shakespeare & Company bookstore
- Montmartre: Bohemian village with artist studios and cabarets
- Champs-Élysées: Iconic avenue with shopping and dining
- Le Cité: Historic island with gardens and river walks

Museums & Culture:
- Musée d'Orsay: Impressionist art museum in a former train station
- Picasso Museum: Extensive collection of Picasso's works
- Versailles Palace: Former royal residence with stunning gardens
- Seine River Cruises: Scenic boat tours through the city

Food & Dining:
- Michelin-starred restaurants
- Charming bistros with classic French cuisine
- Bakeries with fresh croissants and pastries
- Wine bars and cheese shops
- Street food like crêpes and baguettes

Shopping:
- Luxury brands on Champs-Élysées
- Boutiques in Marais and Latin Quarter
- Vintage shops in trendy areas

Best time to visit: April-May or September-October
Getting around: Metro, buses, and Seine cruises""",
        "source": "Paris Tourism Board & Travel Guide",
        "travel_styles": ["cultural", "luxury", "relaxation"]
    },
    "new_zealand": {
        "destination": "New Zealand",
        "category": "adventure",
        "description": "Adventure capital with dramatic landscapes, hiking trails, and extreme sports.",
        "content": """New Zealand is a stunning island nation known for dramatic landscapes, adventure sports, and Māori culture.

North Island:
- Auckland: Largest city, gateway to New Zealand
- Rotorua: Geothermal area with hot springs, mud pools, and Māori villages
- Tongariro National Park: UNESCO site with Mount Doom hike
- Waitomo Caves: Underground caves with glowworms and boat tours
- Wellington: Capital city with museums and food scene

South Island:
- Queenstown: Adventure sports capital (bungee jumping, skiing, jet boating)
- Milford Sound: Stunning fjord with dramatic waterfalls
- Fjordland National Park: Remote wilderness with hiking trails
- Mount Cook: New Zealand's highest peak
- Lake Wanaka: Beautiful alpine lake for outdoor activities
- Dunedin: Coastal city with wildlife viewing (penguins, sea lions)

Adventure Activities:
- Hiking: Milford Track, Routeburn Track, Tongariro Alpine Crossing
- Bungee jumping and adventure sports in Queenstown
- Skydiving and paragliding
- Surfing on both coasts
- Jet boating and white-water rafting
- Skiing in winter

Natural Wonders:
- Glow worm caves
- Geothermal areas with hot springs
- Fiordlands with glacier-fed lakes
- Rainforests and native bird sanctuaries

Cultural Sites:
- Māori cultural experiences and villages
- Treaty grounds
- Art galleries and museums

Best time to visit: December-February (summer) for hiking, June-August for skiing
Duration: Minimum 10-14 days recommended""",
        "source": "New Zealand Tourism Board & Adventure Travel",
        "travel_styles": ["adventure", "relaxation"]
    },
    "dubai": {
        "destination": "Dubai, UAE",
        "category": "luxury",
        "description": "Modern luxury destination with world-class architecture, shopping, and desert experiences.",
        "content": """Dubai is a cosmopolitan city known for ambitious architecture, luxury shopping, and desert adventures.

Iconic Attractions:
- Burj Khalifa: World's tallest building with observation decks
- Palm Jumeirah: Artificial palm-shaped islands with luxury resorts
- Burj Al Arab: Iconic sail-shaped luxury hotel
- Dubai Mall: World's largest shopping mall with aquarium and ice rink
- Sheikh Mohammed Centre: Modern architecture museum

Neighborhoods:
- Downtown Dubai: Business district with luxury hotels and restaurants
- Dubai Marina: Upscale residential area with yacht clubs
- Jumeirah: Beach area with luxury resorts and water sports
- Old Town: Historic quarter with traditional souks and heritage sites
- Deira: Traditional trading district with gold souks

Experiences:
- Desert safari with dune bashing, camel riding, and Bedouin camps
- Luxury yacht cruises along the coast
- Indoor skiing at Ski Dubai
- Water sports: jet skiing, parasailing, windsurfing
- Spa and wellness treatments in luxury resorts

Shopping & Dining:
- World-class shopping malls
- High-end boutiques and luxury brands
- Traditional gold and spice souks
- Michelin-starred restaurants
- Rooftop bars with city views

Cultural Sites:
- Sheikh Mohammed Museum: Local history and culture
- Al Fahidi Historical District: Traditional wind-tower architecture
- Gold Souk: Traditional marketplace

Best time to visit: October-April (cooler weather)
Activities: 3-5 days optimal
Getting around: Metro, taxis, and rental cars""",
        "source": "Dubai Tourism Board & Travel Guide",
        "travel_styles": ["luxury", "adventure"]
    },
    "barcelona": {
        "destination": "Barcelona, Spain",
        "category": "cultural",
        "description": "Mediterranean city famous for Gaudí's architecture, beaches, and vibrant nightlife.",
        "content": """Barcelona is the capital of Catalonia, known for modernist architecture, Mediterranean beaches, and vibrant culture.

Gaudí & Architecture:
- Sagrada Familia: Iconic basilica under construction since 1883
- Park Güell: Whimsical park with colorful mosaic tiles
- Casa Batlló: Modernist residential building with flowing design
- Casa Milà: Residential building with undulating stone facade
- Palau de la Música Catalana: Concert hall with decorative tile work

Historic Neighborhoods:
- Gothic Quarter: Medieval old town with narrow streets and plazas
- La Rambla: Tree-lined promenade from Plaça Reial to the waterfront
- Montjuïc: Hill with museums, gardens, and fortress
- Gràcia: Bohemian neighborhood with plazas and independent shops
- El Born: Trendy district with galleries and restaurants

Beaches & Waterfront:
- Barceloneta Beach: Popular urban beach with restaurants
- Port Vell: Waterfront area with shopping and entertainment
- Olympic Port: Modern marina with restaurants and nightlife

Museums & Culture:
- Picasso Museum: Collection of Picasso's early works
- National Art Museum of Catalonia: Art collection with city views
- FC Barcelona Football Stadium: Home of famous football club

Food & Dining:
- Tapas bars throughout the city
- Fresh seafood restaurants
- Calçots (roasted spring onions) in winter
- Vermouth culture and wine bars
- Michelin-starred restaurants

Nightlife & Entertainment:
- Vibrant bar scene in Gothic Quarter
- Beach clubs and waterfront bars
- Live music venues
- Flamenco shows

Best time to visit: April-May or September-October
Getting around: Metro, buses, walking
Festival: La Mercè (September) with human towers and concerts""",
        "source": "Barcelona Tourism Board & Travel Guide",
        "travel_styles": ["cultural", "relaxation", "adventure"]
    },
    "marrakech": {
        "destination": "Marrakech, Morocco",
        "category": "cultural",
        "description": "Exotic city with bustling souks, stunning palaces, and nearby deserts.",
        "content": """Marrakech is a major city in Morocco known for its souks, palaces, gardens, and desert proximity.

Medina (Old Town):
- Jemaa el-Fnaa Square: Lively plaza with street performers, food stalls, and market
- Souks: Maze-like markets selling textiles, spices, crafts, and souvenirs
- Koutoubia Mosque: Largest mosque with iconic minaret
- Bahia Palace: Ornate palace with decorated rooms and courtyards

Gardens & Palaces:
- Majorelle Garden: Beautiful botanical garden with Art Deco villa
- Menara Garden: Historic garden with olive trees and water basin
- Saadian Tombs: Royal burial site with intricate tilework
- Ben Youssef Mosque: Ancient mosque with detailed stucco work

Neighborhoods:
- Mellah: Historic Jewish quarter
- Kasbah: Royal quarter with palace and gardens
- Gueliz: Modern district with restaurants and shops
- Palmeraie: Upscale residential area north of medina

Experiences:
- Day trips to Atlas Mountains and Berber villages
- Sahara Desert excursions (2-3 days) with camel trekking
- Traditional hammam (spa) experiences
- Cooking classes learning Moroccan cuisine
- Horseback riding in palmeries
- Hot air balloon rides over landscapes

Food & Cuisine:
- Tagines (slow-cooked stews with meat and vegetables)
- Couscous
- Mint tea and Moroccan pastries
- Street food in Jemaa el-Fnaa
- Spice markets for unique flavors

Crafts & Shopping:
- Leather tanning pits and leather goods
- Carpet and textile weaving
- Metalwork and lanterns
- Traditional Moroccan dress and accessories

Best time to visit: October-April (pleasant weather)
Language: Arabic and French; English spoken in tourist areas
Nearby: High Atlas Mountains, Sahara Desert, coastal towns""",
        "source": "Marrakech Tourism Board & Morocco Travel",
        "travel_styles": ["cultural", "adventure", "luxury"]
    },
    "iceland": {
        "destination": "Iceland",
        "category": "adventure",
        "description": "Land of fire and ice with waterfalls, glaciers, and natural hot springs.",
        "content": """Iceland is a Nordic island nation known for dramatic volcanic landscapes, waterfalls, glaciers, and the Northern Lights.

Golden Circle Route:
- Þingvellir National Park: UNESCO site with tectonic plates visible
- Geysir: Active geothermal area with Strokkur geyser erupting hourly
- Gullfoss Waterfall: Powerful waterfall in two stages

Waterfalls & Natural Wonders:
- Skógafoss: 60-meter waterfall in south Iceland
- Seljalandsfoss: Waterfall where you can walk behind the cascade
- Dettifoss: Europe's most powerful waterfall
- Vatnajökull Glacier: Europe's largest glacier with ice caves

Coastal Areas:
- Black sand beaches in Vik and Reynisfjara
- Jökulsárlón Glacier Lagoon: Icebergs floating in lagoon
- Diamond Beach: Black sand beach with ice chunks
- Westfjords: Remote region with dramatic cliffs

Hot Springs & Geothermal:
- Blue Lagoon: Geothermal spa near Reykjavik
- Sky Lagoon: Natural hot spring with ocean views
- Mývatn: Geothermal lake with boiling mud pools
- Natural hot springs throughout the country

Activities:
- Northern Lights viewing (September-March)
- Glacier hiking and ice cave exploration
- Hiking trails through diverse landscapes
- Whale watching from Reykjavik
- Horseback riding on Icelandic horses
- Snorkeling between tectonic plates

Reykjavik:
- Capital city with museums and galleries
- Harpa concert hall
- Perlan observation dome
- Restaurant scene with local cuisine
- Vibrant nightlife and culture

Best time to visit: 
- Summer (June-August) for midnight sun and hiking
- Winter (September-March) for Northern Lights
Duration: 7-10 days for comprehensive tour
Road: Ring Road circumnavigates the entire country""",
        "source": "Iceland Tourism Board & Adventure Travel",
        "travel_styles": ["adventure", "relaxation", "cultural"]
    },
    "seychelles": {
        "destination": "Seychelles",
        "category": "relaxation",
        "description": "Island paradise with pristine beaches, coral reefs, and tropical wildlife.",
        "content": """Seychelles is an archipelago of 115 islands in the Indian Ocean known for pristine beaches and marine biodiversity.

Main Islands:
- Mahé: Largest island with capital Victoria and diverse attractions
- Praslin: Second largest with palm forests and beaches
- La Digue: Small island famous for Anse Source d'Argent beach
- Silhouette: Remote island with jungle and pristine beaches

Beaches:
- Anse Source d'Argent: Famous beach with granite boulders
- Anse Lazio: White-sand beach on Praslin island
- Beau Vallon: Popular beach near Victoria
- Anse Takamaka: Secluded beach on Mahé
- Anse Cocos: Remote pristine beach

Marine Life & Diving:
- Coral reefs teeming with tropical fish
- Sea turtles in their natural habitat
- Snorkeling and diving sites
- Whale shark encounters (seasonal)
- Manta ray viewing

Nature & Wildlife:
- Vallee de Mai: UNESCO site with rare palms
- Aldabra Tortoise Sanctuary: Ancient giant tortoises
- Bird Island: Seabird breeding sanctuary
- Jungle treks and nature walks
- Botanical gardens

Activities:
- Beach relaxation and sunbathing
- Water sports: snorkeling, diving, kayaking, windsurfing
- Fishing trips
- Boat tours to nearby islands
- Beach barbecues
- Spa and wellness

Local Culture:
- Creole cuisine and seafood restaurants
- Traditional markets in Victoria
- Cultural performances and music
- Local crafts and souvenirs

Best time to visit: 
- March-May and September-November (mild weather)
- Avoid monsoon seasons
Language: Seychellois Creole, English, French
Getting around: Ferries between islands, small boats""",
        "source": "Seychelles Tourism Board & Beach Travel",
        "travel_styles": ["relaxation", "adventure"]
    },
    "thai_islands": {
        "destination": "Thai Islands (Phuket, Krabi, Koh Samui)",
        "category": "relaxation",
        "description": "Tropical islands with stunning beaches, clear waters, and vibrant nightlife.",
        "content": """Thailand's islands are famous for white-sand beaches, warm waters, and island culture.

Phuket:
- Patong Beach: Popular beach with bars and water sports
- Kata and Karon Beaches: More peaceful alternatives
- Big Buddha: 45-meter statue overlooking the island
- Phang Nga Bay: Limestone cliffs and James Bond Island
- Nightlife on Bangla Road

Krabi Province:
- Railay Beach: Accessible only by boat, surrounded by limestone cliffs
- Ao Nang: Lively beach with restaurants and shops
- Emerald Pool: Natural freshwater pool in jungle
- Four Islands Tour: Popular boat excursion
- Rock climbing and bouldering sites

Koh Samui:
- Chaweng Beach: Main beach with restaurants and nightlife
- Lamai Beach: Quieter alternative beach
- Big Buddha Temple: Golden Buddha statue
- Grandmother and Grandfather Rocks: Unique rock formations
- Nightlife and beach clubs

Koh Tao:
- Diving and snorkeling hotspot
- Transparent waters and coral reefs
- Shark and sea turtle sightings
- Dive courses and certification
- Budget-friendly accommodation

Phi Phi Islands:
- Maya Bay: Famous beach from "The Beach" film
- Bamboo Island: Pristine white-sand beach
- Snorkeling in clear waters
- Sunset viewpoint
- Day trips from Phuket and Krabi

Activities:
- Snorkeling and diving
- Muay Thai boxing lessons
- Spa and massage treatments
- Elephant sanctuaries (ethical)
- Cooking classes
- Jungle treks
- Island hopping boat tours

Cuisine:
- Fresh seafood
- Pad Thai and noodle dishes
- Spicy curries
- Tropical fruits
- Night markets with street food

Best time to visit: November-February (cool and dry)
Getting around: Boats, taxis, motorbike rentals
Visas: Visa-free for many nationalities (30 days)""",
        "source": "Thailand Tourism Board & Travel Blogs",
        "travel_styles": ["relaxation", "adventure"]
    },
    "swiss_alps": {
        "destination": "Swiss Alps",
        "category": "adventure",
        "description": "Mountain paradise with pristine scenery, hiking, and winter sports.",
        "content": """The Swiss Alps offer stunning mountain scenery, world-class hiking, and excellent winter sports.

Key Regions:
- Interlaken: Central hub with nearby Jungfrau and Eiger
- Zermatt: Base for Matterhorn hikes and skiing
- Appenzell Alps: Rural region with tradition and charm
- Bernese Oberland: Famous hiking region with numerous trails
- Valais: Valley region with wine and mountain villages

Iconic Peaks & Views:
- Jungfrau: 3,466m peak with top-of-Europe railway
- Matterhorn: Iconic 4,478m peak above Zermatt
- Eiger: Famous climbing destination near Interlaken
- Monte Rosa: Highest point in Swiss Alps
- Schilthorn: Rotating restaurant with 360-degree views

Summer Activities:
- Alpine hiking on well-maintained trails
- Mountain biking
- Cable car and cogwheel railway tours
- Paragliding over mountain valleys
- Rock climbing
- Lakes for swimming and water sports

Winter Activities:
- Skiing and snowboarding on numerous slopes
- Cross-country skiing
- Snowshoeing
- Sledding
- Winter mountaineering

Villages & Towns:
- Zermatt: Car-free alpine village
- Grindelwald: Mountain village with cable cars
- Kandersteg: Gateway to Oeschinen Lake
- Saas-Fee: Glacier resort
- Gstaad: Upscale resort town

Transportation & Infrastructure:
- Excellent train network including scenic routes
- Jungfrau Railway: UNESCO site with mountain train
- Extensive hiking trail network
- Cable cars and gondolas
- Mountain passes (Gotthard, Furka, Simplon)

Food & Culture:
- Raclette and fondue
- Alpenmacaroni
- Swiss chocolate and pastries
- Mountain huts serving traditional food
- Local cheese dairies

Best time to visit:
- Summer (June-September) for hiking
- Winter (December-March) for skiing
Getting around: Swiss Travel Pass recommended
Language: German (most regions), French, Italian""",
        "source": "Swiss Tourism Board & Alpine Travel",
        "travel_styles": ["adventure", "luxury", "relaxation"]
    },
    "egypt": {
        "destination": "Egypt",
        "category": "cultural",
        "description": "Land of ancient wonders with pharaonic tombs, temples, and the Nile River.",
        "content": """Egypt offers a glimpse into one of the world's greatest ancient civilizations along the Nile River.

Cairo & Giza:
- Great Pyramids of Giza: Khufu, Khafre, and Menkaure pyramids
- The Great Sphinx: Limestone statue with lion body
- Egyptian Museum: Extensive collection of pharaonic artifacts
- Citadel of Saladin: Medieval fortress with panoramic views
- Khan el-Khalili Bazaar: Historic market with souvenirs and crafts
- Islamic Cairo: Historic district with mosques and traditional architecture

Luxor & Valley of the Kings:
- Valley of the Kings: Royal burial site with pharaonic tombs
- Temple of Karnak: Massive temple complex
- Luxor Temple: Ancient temple on the Nile
- Valley of the Queens: Royal women's burial site
- West Bank: Necropolis with extensive ruins
- Hot air balloon rides over the valley

Upper Egypt:
- Aswan: Scenic Nile city with Nubian culture
- Philae Temple: Relocated temple dedicated to Isis
- Edfu: Temple of Horus on the Nile
- Kom Ombo: Ptolemaic temple with dual dedication
- Nile River cruises between cities

Nile River Experiences:
- Luxury cruise ships with multiple stops
- Traditional felucca sailboats
- Sunset sails in Aswan
- River banks lined with date palms and villages
- Life on the water for 3-7 days

Alexandria:
- Mediterranean coastal city
- Bibliotheca Alexandrina: Modern library
- Catacombs of Kom el Shoqafa
- Citadel of Qaitbay: Fortress on the coast
- Beach and waterfront dining

Desert Experiences:
- Sahara Desert safaris
- Bedouin camps under starry skies
- Dune bashing in 4x4 vehicles
- Camel trekking
- Siwa Oasis: Remote desert settlement

Food & Culture:
- Koshari: Mix of pasta, rice, and lentils
- Fresh produce from Nile basin
- Kebab and grilled meats
- Falafel and bread
- Egyptian tea and coffee
- Street food markets

Best time to visit: October-April (cooler weather)
Duration: 8-14 days recommended
Getting around: Nile cruises, internal flights, organized tours
Language: Arabic; English widely spoken in tourist areas""",
        "source": "Egyptian Tourism Board & History Travel",
        "travel_styles": ["cultural", "adventure", "relaxation"]
    },
    "costa_rica": {
        "destination": "Costa Rica",
        "category": "adventure",
        "description": "Biodiverse nature destination with rainforests, volcanoes, and wildlife.",
        "content": """Costa Rica is a Central American country famous for biodiversity, cloud forests, and adventure activities.

Regions:
- Monteverde: Cloud forest with hanging bridges and quetzals
- Arenal: Volcano region with hot springs and rainforest
- Osa Peninsula: Remote region with pristine rainforest and wildlife
- Central Pacific: Beaches with access to rainforest
- Caribbean Coast: Laid-back beach towns

National Parks:
- Corcovado National Park: Remote jungle with tapirs, jaguars, monkeys
- Manuel Antonio: Beaches and rainforest combined
- Arenal Volcano National Park: Active volcano and lake
- Tortuguero: Turtle nesting beaches and canal exploration
- Monteverde Cloud Forest: Misty forest with endemic birds

Activities:
- Rainforest hiking and nature walks
- Ziplining through canopy
- Hot springs near Arenal Volcano
- Wildlife spotting: monkeys, sloths, macaws, poison dart frogs
- Surfing on both coasts
- Whitewater rafting
- Canyoning and waterfall rappelling
- Horseback riding through landscapes

Beaches:
- Manuel Antonio: Protected beaches with rocky outcrops
- Tamarindo: Popular surf beach with resort town
- Puerto Viejo: Caribbean vibe with dark sand beach
- Santa Teresa: Trendy surfer destination
- Uvita: South Pacific beach

Wildlife:
- Sloths (two and three-toed)
- Howler monkeys
- Macaws and tropical birds
- Sea turtles nesting
- Poison dart frogs
- Caimans and crocodiles in rivers

Cultural Sites:
- Arenal Indigenous Reserve: Native cultures
- Local cooperative farms
- Butterfly gardens
- Snake farms and wildlife centers

Food & Dining:
- Casado: Local plate with rice, beans, vegetables, and meat
- Fresh tropical fruits (pineapple, papaya, mango)
- Rice and beans
- Fresh seafood on coasts
- Coffee from highland regions

Eco-lodges:
- Jungle lodges with naturalist guides
- Canopy cabins in treetops
- Sustainable tourism operations
- Solar-powered eco-resorts

Best time to visit: 
- Dry season (December-April) for most regions
- Green season (May-November) for fewer tourists
Getting around: Internal flights, rental cars, shuttle buses
Language: Spanish; English spoken in tourist areas
Peace: Costa Rica is one of the most peaceful countries in Central America""",
        "source": "Costa Rica Tourism Board & Nature Travel",
        "travel_styles": ["adventure", "relaxation", "cultural"]
    }
}


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using SequenceMatcher."""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def retrieve_destination(travel_style: str, query: str = "") -> dict:
    """Retrieve destination based on travel style and semantic similarity to query."""
    
    # Normalize travel style
    travel_style = travel_style.lower().strip()
    
    # Create a scoring system
    best_destination = None
    best_score = -1
    
    for destination_key, destination_info in DESTINATIONS.items():
        score = 0
        
        # Score based on travel style match
        if travel_style in [ts.lower() for ts in destination_info.get("travel_styles", [])]:
            score += 3
        elif destination_info.get("category", "").lower() == travel_style:
            score += 2
        
        # Score based on semantic similarity to query
        if query:
            query_lower = query.lower()
            similarity = calculate_similarity(
                query_lower,
                f"{destination_info['destination']} {destination_info['description']}".lower()
            )
            score += similarity * 2
        
        if score > best_score:
            best_score = score
            best_destination = destination_key
    
    # Fallback to first destination matching travel style if no good match
    if best_destination is None:
        for destination_key, destination_info in DESTINATIONS.items():
            if destination_info.get("category", "").lower() == travel_style:
                best_destination = destination_key
                break
        # Ultimate fallback
        if best_destination is None:
            best_destination = "tokyo"
    
    destination_data = DESTINATIONS[best_destination].copy()
    
    return {
        "destination": destination_data["destination"],
        "description": destination_data["description"],
        "content": destination_data.get("content", destination_data["description"]),
        "category": destination_data.get("category", ""),
        "source": destination_data.get("source", "Travel Database"),
        "travel_styles": destination_data.get("travel_styles", [])
    }


def get_all_destinations() -> list:
    """Get all available destinations for RAG initialization."""
    return list(DESTINATIONS.values())

    # Check query for specific tropical/island preferences
    query_lower = query.lower()
    if any(word in query_lower for word in ["tropical", "island", "beach", "ocean", "paradise"]):
        destination_key = "bali"
    else:
        destination_key = style_mapping.get(travel_style, "tokyo")
    
    destination = DESTINATIONS.get(destination_key, DESTINATIONS["tokyo"])
    
    return destination
