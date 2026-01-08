from pipeline.ingestion.daily_loader import load_daily_reviews

if __name__ == "__main__":
    reviews = load_daily_reviews("2024-07-15")

    print("Total reviews:", len(reviews))
    print("Sample reviews:")
    for r in reviews[:3]:
        print(r)
