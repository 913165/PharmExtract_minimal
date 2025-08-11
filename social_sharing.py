"""
Social sharing configuration and utilities for RadExtract.

This module handles all social media sharing functionality including
URL generation, message formatting, and platform-specific configurations.
"""

from urllib.parse import quote_plus


class SocialSharingConfig:
    """Configuration and utilities for social media sharing."""

    # Production URL for consistent sharing
    PRODUCTION_URL = "https://google-radextract.hf.space"

    # Twitter/X share message
    TWITTER_MESSAGE = (
        "Check out this new demo from @AkshayGoelMD and the team @GoogleResearch: Gemini + LangExtract structure & optimize radiology reports.\n\n"
        "Try it here! → https://google-radextract.hf.space \n\n"
        "#Gemini #LangExtract #RadExtract #OpenSource #Google #Radiology"
    )

    # LinkedIn sharing content
    LINKEDIN_TITLE = "RadExtract – Radiology Report Structuring Demo"
    LINKEDIN_SUMMARY = "Gemini-powered radiology report structuring demo"

    @classmethod
    def get_sharing_context(cls, request_url_root):
        """
        Generate all social sharing variables for template rendering.

        Args:
            request_url_root: The root URL from Flask request

        Returns:
            dict: All variables needed for social sharing in templates
        """
        page_url = request_url_root.rstrip("/")

        # Use production URL for sharing (consistent experience, localhost won't work for previews)
        share_url_for_sharing = (
            cls.PRODUCTION_URL if "localhost" in page_url else page_url
        )

        return {
            "share_url": page_url,
            "share_url_for_sharing": share_url_for_sharing,
            "share_url_encoded": quote_plus(share_url_for_sharing),
            "share_text": quote_plus(cls.TWITTER_MESSAGE),
            "linkedin_title": quote_plus(cls.LINKEDIN_TITLE),
            "linkedin_summary": quote_plus(cls.LINKEDIN_SUMMARY),
        }
