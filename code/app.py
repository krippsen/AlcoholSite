from py2neo import Graph, Node, Relationship
from flask import Flask, render_template, request, redirect
from random import choice


app = Flask(__name__)
graph = Graph("bolt://neo4j:7687", auth=("neo4j", "adminpass"))

logged_user = "Pepa"

def mock_data(graph):
    tx = graph.begin()

    graph.run("MATCH (n) -[r] -> () DELETE n, r")
    graph.run("MATCH (n) DELETE n")

    pepa = Node("Person", name="Pepa", age=34, hobbies=["programming", "running"],
                preferences=["Beer", "Whiskey"],
                favorite_places=["Bar A", "Pub B"],
                tasting_notes=["Loved the IPA at Bar A"],
                posts=["Enjoyed the new stout!"])

    jana = Node("Person", name="Jana", age=30, hobbies=["cats", "running"],
                preferences=["Wine", "Gin"],
                favorite_places=["Wine House"],
                tasting_notes=["Excellent Merlot at Wine House"],
                posts=["Had a lovely evening!"])

    michal = Node("Person", name="Michal", age=38, hobbies=["partying", "cats"],
                  preferences=["Vodka"],
                  favorite_places=["Club X"],
                  tasting_notes=["Great cocktails at Club X"],
                  posts=["What a night!"])

    alena = Node("Person", name="Alena", age=32, hobbies=["kids", "cats"],
                 preferences=["Non-alcoholic"],
                 favorite_places=["Cafe Z"],
                 tasting_notes=["Delicious mocktails at Cafe Z"],
                 posts=["Family time is the best."])

    richard = Node("Person", name="Richard", age=33, hobbies=["partying", "cats"],
                   preferences=["Tequila"],
                   favorite_places=["Bar Y"],
                   tasting_notes=["Strong shots at Bar Y"],
                   posts=["Party never stops!"])

    users = [pepa, jana, michal, alena, richard]

    relationships = [
        Relationship(pepa, "LIKES", jana),
        Relationship(jana, "LIKES", pepa),
        Relationship(michal, "LIKES", alena),
        Relationship(alena, "DISLIKES", michal),
        Relationship(alena, "LIKES", pepa),
        Relationship(richard, "LIKES", alena)
    ]

    for user in users:
        graph.create(user)

    for relationship in relationships:
        graph.create(relationship)


def get_user_node(graph, name):
    return graph.evaluate(f"""
        MATCH (user:Person)
        WHERE user.name = '{name}'
        RETURN user
    """)

def get_logged_user_profile(graph, username):
    return graph.run(f"""
        MATCH (user:Person)
        WHERE user.name = '{username}'
        RETURN user.name, user.age, user.hobbies,
               user.preferences, user.favorite_places,
               user.tasting_notes, user.posts
    """).data()[0]
    
            
def get_matches(graph, username):
    return graph.run(f"""
        MATCH (friend:Person)-[:LIKES]->(user:Person)-[:LIKES]->(friend:Person) 
        WHERE user.name = '{username}'
        RETURN friend.name, friend.age, friend.hobbies
    """).data()


def available_matches(graph, username):
    return graph.run(f"""
        MATCH (user:Person)
        MATCH (friend:Person)
        WHERE user.name = '{username}'
        AND NOT (user:Person)-[:LIKES]->(friend:Person)
        AND NOT (friend:Person)-[:DISLIKES]->(user:Person)
        AND NOT (user:Person)-[:DISLIKES]->(friend:Person)
        AND NOT friend.name = '{username}'
        RETURN friend.name, friend.age, friend.hobbies
    """).data()


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
@app.route("/home")
def hello_world():
    logged_user_info = get_logged_user_profile(graph, logged_user)
    num_of_matches = len(get_matches(graph, logged_user))
    num_of_available_matches = len(available_matches(graph, logged_user)) 
    return render_template("home.html", profile=logged_user_info, num_of_matches=num_of_matches, num_of_available_matches=num_of_available_matches)


@app.route("/matches")
def matches():
    matches = get_matches(graph, logged_user)
    return render_template("matches.html", profiles=matches)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        potential_matches = available_matches(graph, logged_user)
        if potential_matches:
            random_profile = choice(potential_matches)
        else:
            random_profile = None
        return render_template("search.html", profile=random_profile)
    else:
        date_choice = request.form.get("date_choice")
        friend_name = request.form.get("friend_name")
        user_node = get_user_node(graph, logged_user)
        friend_node = get_user_node(graph, friend_name)
        if date_choice == "like":
            new_relationship = Relationship(user_node, "LIKES", friend_node)
        elif date_choice == "dislike":
            new_relationship = Relationship(user_node, "DISLIKES", friend_node)
        graph.create(new_relationship)
        return redirect("/search")


@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if request.method == "POST":
        preferences = request.form.getlist("preferences")
        favorite_places = request.form.getlist("favorite_places")
        tasting_notes = request.form.getlist("tasting_notes")
        posts = request.form.getlist("posts")
        graph.run(f"""
            MATCH (user:Person)
            WHERE user.name = '{logged_user}'
            SET user.preferences = {preferences},
                user.favorite_places = {favorite_places},
                user.tasting_notes = {tasting_notes},
                user.posts = {posts}
        """)
        return redirect("/home")
    else:
        profile = get_logged_user_profile(graph, logged_user)
        return render_template("edit_profile.html", profile=profile)


if __name__ == "__main__":
    mock_data(graph)
    app.run(debug=True, host="0.0.0.0", port=5000)