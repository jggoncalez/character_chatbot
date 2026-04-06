import pytest
from tests.conftest import Colors

@pytest.mark.api
def test_get_feed(client):
    """Test GET /feed generates new feed posts on demand"""
    print(f"\n{Colors.BLUE}Testing: GET /feed (generates posts){Colors.ENDC}")
    
    response = client.get("/feed")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "posts" in data, "Response missing 'posts' field"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    posts = data.get("posts", [])
    print(f"  Posts generated: {Colors.YELLOW}{len(posts)}{Colors.ENDC}")
    for i, post in enumerate(posts[:3], 1):
        char = post.get('character', 'Unknown')
        text = post.get('text', '')[:60]
        print(f"    {i}. [{Colors.CYAN}{char}{Colors.ENDC}] {text}...")

@pytest.mark.api
def test_get_feed_cached(client):
    """Test GET /feed/cached returns cached feed without generating new posts"""
    print(f"\n{Colors.BLUE}Testing: GET /feed/cached (retrieves cached posts){Colors.ENDC}")
    
    response = client.get("/feed/cached")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "posts" in data, "Response missing 'posts' field"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    posts = data.get("posts", [])
    print(f"  Cached posts: {Colors.YELLOW}{len(posts)}{Colors.ENDC}")
    if posts:
        print(f"    Sample posts:")
        for i, post in enumerate(posts[:2], 1):
            char = post.get('character', 'Unknown')
            comments = len(post.get('comments', []))
            text = post.get('text', '')[:50]
            print(f"    {i}. [{Colors.CYAN}{char}{Colors.ENDC}] {text}... ({comments} comments)")
    else:
        print(f"    {Colors.YELLOW}No cached posts available{Colors.ENDC}")

@pytest.mark.api
def test_feed_comment(client):
    """Test POST /feed/comment adds comment to existing post"""
    print(f"\n{Colors.BLUE}Testing: POST /feed/comment{Colors.ENDC}")
    
    # Get cached feed to find a post
    feed = client.get("/feed/cached").json()
    posts = feed.get("posts", [])

    if not posts:
        pytest.skip("Nenhum post no feed pra testar comentário")

    post_id = posts[0]["id"]
    comment_text = "Comentário de teste automático!"
    
    response = client.post("/feed/comment", json={
        "post_id": post_id,
        "text": comment_text
    })
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Post ID: {Colors.CYAN}{post_id}{Colors.ENDC}")
    print(f"  Comment: '{comment_text}'")
    data = response.json()
    if 'comments' in data:
        print(f"  Total comments: {Colors.YELLOW}{len(data['comments'])}{Colors.ENDC}")

@pytest.mark.api
def test_feed_comment_not_found(client):
    """Test POST /feed/comment with non-existent post returns 404"""
    print(f"\n{Colors.BLUE}Testing: POST /feed/comment with invalid post (should fail){Colors.ENDC}")

    response = client.post("/feed/comment", json={
        "post_id": "id-inexistente-12345",
        "text": "Teste"
    })

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Error: {response.json().get('detail', 'Post not found')}")

@pytest.mark.api
def test_create_user_post(client):
    """Test POST /feed/post creates a user post with character comments"""
    print(f"\n{Colors.BLUE}Testing: POST /feed/post (create user post){Colors.ENDC}")

    user_text = "Qual é a melhor linguagem de programação?"
    response = client.post("/feed/post", json={"text": user_text})

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()

    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Post Author: {Colors.CYAN}{data.get('character', 'Unknown')}{Colors.ENDC}")
    print(f"  Post Text: '{data.get('text', '')}'")

    assert data.get("character") == "user", "Post should be from 'user'"
    assert data.get("text") == user_text, "Post text should match"
    assert "comments" in data, "Post should have comments"

    comments = data.get("comments", [])
    print(f"  Comments generated: {Colors.YELLOW}{len(comments)}{Colors.ENDC}")
    for i, comment in enumerate(comments, 1):
        char = comment.get('character', 'Unknown')
        text = comment.get('text', '')[:60]
        print(f"    {i}. [{Colors.CYAN}{char}{Colors.ENDC}] {text}...")

@pytest.mark.api
def test_create_user_post_too_short(client):
    """Test POST /feed/post with text too short returns 422"""
    print(f"\n{Colors.BLUE}Testing: POST /feed/post with empty text (should fail){Colors.ENDC}")

    response = client.post("/feed/post", json={"text": ""})

    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Error: Validation error for empty text")

@pytest.mark.api
def test_create_user_post_too_long(client):
    """Test POST /feed/post with text too long returns 422"""
    print(f"\n{Colors.BLUE}Testing: POST /feed/post with text too long (should fail){Colors.ENDC}")

    long_text = "A" * 501  # max_length is 500
    response = client.post("/feed/post", json={"text": long_text})

    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print(f"  Status: {Colors.GREEN}{response.status_code}{Colors.ENDC}")
    print(f"  Error: Validation error for text too long")