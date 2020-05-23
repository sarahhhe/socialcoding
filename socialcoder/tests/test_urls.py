from django.test import SimpleTestCase
from django.urls import reverse, resolve
from socialcoder.views import feed, leaderboard, add_post, add_comment, add_category, upvote, downvote

class TestUrls(SimpleTestCase):

    def test_feed_url_is_resolved(self):
        url = reverse('socialcoder-feed')
        self.assertEquals(resolve(url).func, feed)

    def test_leaderboard_url_is_resolved(self):
        url = reverse('socialcoder-leaderboard')
        self.assertEquals(resolve(url).func, leaderboard)

    def test_add_post_url_is_resolved(self):
        url = reverse('socialcoder-post-create')
        self.assertEquals(resolve(url).func, add_post)

    def test_add_comment_url_is_resolved(self):
        url = reverse('socialcoder-add-comment', args=[3])
        self.assertEquals(resolve(url).func, add_comment)

    def test_add_category_url_is_resolved(self):
        url = reverse('socialcoder-category-create')
        self.assertEquals(resolve(url).func, add_category)

    def test_upvote_url_is_resolved(self):
        url = reverse('socialcoder-upvote', args=[3])
        self.assertEquals(resolve(url).func, upvote)

    def test_downvote_url_is_resolved(self):
        url = reverse('socialcoder-downvote', args=[3])
        self.assertEquals(resolve(url).func, downvote)
