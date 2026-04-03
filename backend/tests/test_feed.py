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