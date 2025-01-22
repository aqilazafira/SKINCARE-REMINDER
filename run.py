from app import create_app, db

app = create_app()

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    #     from app.seed import seed_data
    #     seed_data() 
    app.run(debug=True)
