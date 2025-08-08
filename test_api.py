#!/usr/bin/env python3
"""
Test script for the Image Attachment Service API
This script demonstrates how to use the API endpoints
"""

import requests
import json
import os
from PIL import Image
import io

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "testuser"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"

def create_test_image():
    """Create a simple test image for upload"""
    # Create a simple 100x100 red image
    img = Image.new('RGB', (100, 100), color='red')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_api():
    """Test the API endpoints"""
    print("🚀 Testing Image Attachment Service API")
    print("=" * 50)
    
    # Test 1: Register user
    print("\n1. Testing user registration...")
    try:
        response = requests.post(f"{BASE_URL}/register", json={
            "username": TEST_USERNAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        if response.status_code == 200:
            print("✅ User registered successfully")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
        elif response.status_code == 400:
            print("ℹ️  User already exists, continuing with login...")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on http://localhost:8000")
        return
    
    # Test 2: Login
    print("\n2. Testing login...")
    try:
        response = requests.post(f"{BASE_URL}/token", data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD
        })
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("✅ Login successful")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 3: Get user info
    print("\n3. Testing user info retrieval...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        
        if response.status_code == 200:
            user_info = response.json()
            print("✅ User info retrieved successfully")
            print(f"   Username: {user_info['username']}")
            print(f"   Email: {user_info['email']}")
        else:
            print(f"❌ Failed to get user info: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ User info error: {e}")
        return
    
    # Test 4: Upload image
    print("\n4. Testing image upload...")
    try:
        test_image = create_test_image()
        files = {"file": ("test_image.jpg", test_image, "image/jpeg")}
        data = {"description": "Test image uploaded via API"}
        
        response = requests.post(f"{BASE_URL}/upload", headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            upload_result = response.json()
            print("✅ Image uploaded successfully")
            print(f"   Image ID: {upload_result['id']}")
            print(f"   Filename: {upload_result['filename']}")
            print(f"   Size: {upload_result['file_size']} bytes")
            print(f"   Download URL: {upload_result['download_url']}")
            
            # Store image info for later tests
            image_id = upload_result['id']
            filename = upload_result['filename']
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return
    
    # Test 5: List images
    print("\n5. Testing image listing...")
    try:
        response = requests.get(f"{BASE_URL}/images", headers=headers)
        
        if response.status_code == 200:
            images = response.json()
            print("✅ Images listed successfully")
            print(f"   Found {len(images)} images")
            for img in images:
                print(f"   - {img['original_filename']} ({img['file_size']} bytes)")
        else:
            print(f"❌ Failed to list images: {response.status_code}")
    except Exception as e:
        print(f"❌ List images error: {e}")
    
    # Test 6: Get specific image
    print("\n6. Testing specific image retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/images/{image_id}", headers=headers)
        
        if response.status_code == 200:
            image_info = response.json()
            print("✅ Image details retrieved successfully")
            print(f"   Description: {image_info['description']}")
            print(f"   Uploaded at: {image_info['uploaded_at']}")
        else:
            print(f"❌ Failed to get image details: {response.status_code}")
    except Exception as e:
        print(f"❌ Get image error: {e}")
    
    # Test 7: Download image
    print("\n7. Testing image download...")
    try:
        response = requests.get(f"{BASE_URL}/download/{filename}", headers=headers)
        
        if response.status_code == 200:
            print("✅ Image download successful")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Content-Length: {response.headers.get('content-length')} bytes")
        else:
            print(f"❌ Download failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Download error: {e}")
    
    # Test 8: Delete image
    print("\n8. Testing image deletion...")
    try:
        response = requests.delete(f"{BASE_URL}/images/{image_id}", headers=headers)
        
        if response.status_code == 200:
            print("✅ Image deleted successfully")
        else:
            print(f"❌ Deletion failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Deletion error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\nYou can now:")
    print("- Visit http://localhost:8000/docs for interactive API documentation")
    print("- Use the API endpoints in your applications")
    print("- Upload, manage, and download images securely")

if __name__ == "__main__":
    test_api()
