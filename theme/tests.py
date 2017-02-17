from datetime import datetime, timedelta

from django.test import TestCase

from .models import Theme, Video, Comment, Thumb


class ThemeTestCase(TestCase):
    def insert_many_comments(self):
        is_positive = True
        for i in range(0, 10):
            Comment.objects.create(
                is_positive=is_positive,
                comment='LoremIpsum {}'.format(i),
                video=self.video
            )
            if is_positive:
                is_positive = False
            else:
                is_positive = True

    def insert_many_thumbs(self):
        is_positive = True
        for i in range(0, 10):
            Thumb.objects.create(
                is_positive=is_positive,
                video=self.video
            )

            if is_positive:
                is_positive = False
            else:
                is_positive = True

    def setUp(self):
        self.theme1 = Theme.objects.create(
            name='TestTheme'
        )
        self.theme2 = Theme.objects.create(
            name='TestTheme2'
        )
        self.theme3 = Theme.objects.create(
            name='TestTheme3'
        )
        self.video = Video.objects.create(
            title='TestVideo',
            date_uploaded=datetime.now(),
            views=50
        )
        self.video.theme.add(self.theme1)
        self.video.theme.add(self.theme2)
        self.video.theme.add(self.theme3)

        self.comment = Comment.objects.create(
            is_positive=True,
            comment='LoremIpsum',
            video=self.video
        )

        self.thumb = Thumb.objects.create(
            time=datetime.now(),
            video=self.video
        )

        self.insert_many_comments()
        self.insert_many_thumbs()

    def test_create_theme(self):
        """Theme should exist."""
        self.assertTrue(Theme.objects.exists())

    def test_total_theme(self):
        """Total themes should be 3."""
        self.assertEqual(Theme.objects.all().count(), 3)

    def test_create_video(self):
        """Video should exist."""
        self.assertTrue(Video.objects.exists())
        self.assertEqual(self.video.views, 50)

    def test_add_themes(self):
        """Should have 3 themes."""
        self.assertEqual(self.video.theme.count(), 3)

    def test_add_comment(self):
        """Add a comment."""
        self.assertTrue(self.video.comments.all()[0].is_positive)

    def test_comment_data(self):
        """Comment should be LoremIpsum."""
        comment = self.video.comments.get(pk=1)
        self.assertEqual(comment.comment, 'LoremIpsum')

    def test_qtd_comments(self):
        """Should have 11 comments."""
        self.assertEqual(Comment.objects.filter(video=self.video).count(), 11)

    def test_postive_comments(self):
        """Should have 6 positive comments."""
        self.assertEqual(
            Comment.objects.filter(
                video=self.video,
                is_positive=True).count(), 6
        )

    def test_negative_comments(self):
        """Should have 5 negatives."""
        self.assertEqual(
            Comment.objects.filter(
                video=self.video,
                is_positive=False
            ).count(), 5
        )

    def test_thumb_exists(self):
        """Thumb should exist."""
        self.assertTrue(Thumb.objects.exists())

    def test_thumb_is_negative(self):
        """First thumb must be negative."""
        thumb = Thumb.objects.get(pk=1)
        self.assertFalse(thumb.is_positive)

    def test_negative_thumbs(self):
        """Should have 6 negative thumbs."""
        self.assertEqual(
            Thumb.objects.filter(
                video=self.video,
                is_positive=False).count(), 6)

    def test_positive_thumbs(self):
        """Should have 5 positive thumbs."""
        self.assertEqual(
            Thumb.objects.filter(
                video=self.video,
                is_positive=True
            ).count(), 5
        )



