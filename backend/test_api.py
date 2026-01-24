#!/usr/bin/env python3
"""
Test script for the /api/v1/all endpoint
Run this after starting the server with: uvicorn app.main:app --reload
"""

import asyncio
import json

import httpx


async def test_endpoint():
    """Test the /api/v1/all endpoint"""

    print("🧪 Testing FastAPI endpoint...")
    print("=" * 50)

    try:
        async with httpx.AsyncClient() as client:
            # Test health endpoint first
            print("\n1. Testing health endpoint...")
            response = await client.get("http://localhost:8000/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")

            # Test main endpoint
            print("\n2. Testing /api/v1/all endpoint...")
            response = await client.get("http://localhost:8000/api/v1/all")

            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print("   ✓ Response received successfully")

                # Validate structure
                required_keys = [
                    "about",
                    "vinylGenres",
                    "vinyl",
                    "books",
                    "coffeeBrands",
                    "coffee",
                    "figures",
                    "projects",
                    "publications",
                    "infographics",
                    "plants",
                    "media",
                ]

                print("\n3. Validating response structure...")
                missing_keys = [key for key in required_keys if key not in data]

                if missing_keys:
                    print(f"   ❌ Missing keys: {missing_keys}")
                    return False
                else:
                    print("   ✓ All required keys present")

                # Check data types
                print("\n4. Validating data types...")

                checks = [
                    ("about.bio", isinstance(data["about"]["bio"], str)),
                    ("vinylGenres is list", isinstance(data["vinylGenres"], list)),
                    ("vinyl is list", isinstance(data["vinyl"], list)),
                    ("books is list", isinstance(data["books"], list)),
                    ("coffeeBrands is list", isinstance(data["coffeeBrands"], list)),
                    ("coffee is list", isinstance(data["coffee"], list)),
                    ("figures is list", isinstance(data["figures"], list)),
                    ("projects is list", isinstance(data["projects"], list)),
                    ("publications is list", isinstance(data["publications"], list)),
                    ("infographics is list", isinstance(data["infographics"], list)),
                    ("plants is list", isinstance(data["plants"], list)),
                    ("media is dict", isinstance(data["media"], dict)),
                ]

                all_valid = True
                for check_name, is_valid in checks:
                    status = "✓" if is_valid else "❌"
                    print(f"   {status} {check_name}")
                    if not is_valid:
                        all_valid = False

                # Check nested structures
                print("\n5. Checking nested structures...")

                if data["vinyl"]:
                    vinyl = data["vinyl"][0]
                    vinyl_checks = [
                        "id" in vinyl and isinstance(vinyl["id"], str),
                        "artist" in vinyl and isinstance(vinyl["artist"], str),
                        "title" in vinyl and isinstance(vinyl["title"], str),
                        "genres" in vinyl and isinstance(vinyl["genres"], list),
                    ]
                    print(
                        f"   Vinyl record structure: {'✓' if all(vinyl_checks) else '❌'}"
                    )

                if data["coffee"]:
                    coffee = data["coffee"][0]
                    coffee_checks = [
                        "id" in coffee and isinstance(coffee["id"], str),
                        "brandId" in coffee and isinstance(coffee["brandId"], str),
                        "name" in coffee and isinstance(coffee["name"], str),
                        "reviews" in coffee and isinstance(coffee["reviews"], list),
                    ]
                    print(f"   Coffee structure: {'✓' if all(coffee_checks) else '❌'}")

                    if coffee["reviews"]:
                        review = coffee["reviews"][0]
                        review_checks = [
                            "method" in review and isinstance(review["method"], str),
                            "rating" in review
                            and (
                                isinstance(review["rating"], (int, float))
                                or review["rating"] is None
                            ),
                        ]
                        print(
                            f"   Coffee review structure: {'✓' if all(review_checks) else '❌'}"
                        )

                # Print summary statistics
                print("\n6. Data summary:")
                print(f"   Vinyl genres: {len(data['vinylGenres'])}")
                print(f"   Vinyl records: {len(data['vinyl'])}")
                print(f"   Books: {len(data['books'])}")
                print(f"   Coffee brands: {len(data['coffeeBrands'])}")
                print(f"   Coffee varieties: {len(data['coffee'])}")
                print(f"   Figures: {len(data['figures'])}")
                print(f"   Projects: {len(data['projects'])}")
                print(f"   Publications: {len(data['publications'])}")
                print(f"   Infographics: {len(data['infographics'])}")
                print(f"   Plants: {len(data['plants'])}")
                print(f"   Media links: {len(data['media']['links'])}")

                # Save sample response
                with open("api_response_sample.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print("\n   📄 Sample response saved to api_response_sample.json")

                print("\n" + "=" * 50)
                if all_valid:
                    print("✅ All tests passed! Endpoint is working correctly.")
                else:
                    print("⚠️  Some validation checks failed. Check the output above.")

                return all_valid

            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                return False

    except Exception as e:
        print(f"\n❌ Error connecting to server: {e}")
        print("\nMake sure the server is running:")
        print("  uvicorn app.main:app --reload")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_endpoint())
    exit(0 if result else 1)
