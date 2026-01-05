from dataclasses import dataclass
from typing import List, Optional

from social.models import Platform, SocialAccount


@dataclass
class AccountAvailability:
    social_account_id: int
    display_name: str
    available: bool
    reason: Optional[str]
    requires_action: Optional[bool] = None
    action_hint: Optional[str] = None


@dataclass
class PlatformAvailability:
    platform: str
    available: bool
    reason: Optional[str]
    accounts: List[AccountAvailability]
    requires_action: Optional[bool] = None
    action_hint: Optional[str] = None


REASON_NO_ACCOUNT = 'No connected account.'
REASON_IG_PRO_REQUIRED = 'Instagram requires a Professional account for publishing.'
REASON_IG_PERMS_MISSING = 'Instagram publishing permissions are missing or invalid.'
REASON_FB_PAGE_REQUIRED = 'Facebook publishing requires a connected Page.'
REASON_TIKTOK_PREREQS = 'TikTok prerequisites or domain verification incomplete.'
REASON_TIKTOK_PHOTO_DISABLED = 'TikTok photo posting not enabled for this account.'
REASON_TIKTOK_TEXT_UNSUPPORTED = 'TikTok supports photo and video posts only.'
REASON_YT_VIDEO_ONLY = 'YouTube supports video uploads only.'
REASON_LINKEDIN_SCOPE = 'Requires additional LinkedIn API access/scope.'
REASON_X_MEDIA_DISABLED = 'X media upload not enabled for current API tier/config.'

ACTION_IG_PRO = 'Switch IG to Business account.'
ACTION_IG_PERMS = 'Reconnect Instagram and grant publishing permissions.'
ACTION_FB_PAGE = 'Connect a Facebook Page.'
ACTION_TIKTOK_PREREQS = 'Complete TikTok domain verification and prerequisites.'
ACTION_TIKTOK_PHOTO = 'Enable TikTok photo posting in Content Posting API.'
ACTION_LINKEDIN = 'Request LinkedIn video permission.'
ACTION_X_MEDIA = 'Configure X tier for media.'
ACTION_CONNECT_ACCOUNT = 'Connect account.'


def evaluate_availability(user, content_type, optional_media_metadata=None):
    accounts = SocialAccount.objects.filter(user=user).order_by('id')
    accounts_by_platform = {platform.value: [] for platform in Platform}
    for account in accounts:
        accounts_by_platform.setdefault(account.platform, []).append(account)

    results = []
    for platform in Platform:
        platform_accounts = accounts_by_platform.get(platform.value, [])
        if platform == Platform.INSTAGRAM:
            results.append(_evaluate_instagram(platform_accounts, content_type))
        elif platform == Platform.FACEBOOK:
            results.append(_evaluate_facebook(platform_accounts, content_type))
        elif platform == Platform.TIKTOK:
            results.append(_evaluate_tiktok(platform_accounts, content_type))
        elif platform == Platform.YOUTUBE:
            results.append(_evaluate_youtube(platform_accounts, content_type))
        elif platform == Platform.LINKEDIN:
            results.append(_evaluate_linkedin(platform_accounts, content_type))
        elif platform == Platform.X:
            results.append(_evaluate_x(platform_accounts, content_type))
        else:
            results.append(PlatformAvailability(platform=platform.value, available=False, reason=REASON_NO_ACCOUNT, accounts=[]))

    return results


def _platform_from_accounts(platform_value, account_availabilities, default_reason):
    available = any(account.available for account in account_availabilities)
    reason = None if available else default_reason
    requires_action = None
    action_hint = None
    if not available and account_availabilities:
        selected = _select_reason(account_availabilities)
        reason = selected.reason
        requires_action = selected.requires_action
        action_hint = selected.action_hint
    elif not available and not account_availabilities and default_reason == REASON_NO_ACCOUNT:
        requires_action = True
        action_hint = ACTION_CONNECT_ACCOUNT
    return PlatformAvailability(
        platform=platform_value,
        available=available,
        reason=reason,
        accounts=account_availabilities,
        requires_action=requires_action,
        action_hint=action_hint,
    )


def _select_reason(account_availabilities):
    for account in account_availabilities:
        if not account.available and account.reason:
            return account
    return account_availabilities[0]


def _evaluate_instagram(accounts, content_type):
    account_availabilities = []
    for account in accounts:
        if account.account_type != SocialAccount.AccountType.INSTAGRAM_PROFESSIONAL:
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_IG_PRO_REQUIRED,
                    requires_action=True,
                    action_hint=ACTION_IG_PRO,
                )
            )
            continue
        if not account.permissions_valid:
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_IG_PERMS_MISSING,
                    requires_action=True,
                    action_hint=ACTION_IG_PERMS,
                )
            )
            continue
        account_availabilities.append(
            AccountAvailability(
                social_account_id=account.id,
                display_name=account.display_name,
                available=True,
                reason=None,
            )
        )
    default_reason = REASON_NO_ACCOUNT if not accounts else REASON_IG_PRO_REQUIRED
    return _platform_from_accounts(Platform.INSTAGRAM.value, account_availabilities, default_reason)


def _evaluate_facebook(accounts, content_type):
    account_availabilities = []
    for account in accounts:
        if account.account_type != SocialAccount.AccountType.FACEBOOK_PAGE:
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_FB_PAGE_REQUIRED,
                    requires_action=True,
                    action_hint=ACTION_FB_PAGE,
                )
            )
            continue
        account_availabilities.append(
            AccountAvailability(
                social_account_id=account.id,
                display_name=account.display_name,
                available=True,
                reason=None,
            )
        )
    default_reason = REASON_NO_ACCOUNT if not accounts else REASON_FB_PAGE_REQUIRED
    return _platform_from_accounts(Platform.FACEBOOK.value, account_availabilities, default_reason)


def _evaluate_tiktok(accounts, content_type):
    account_availabilities = []
    for account in accounts:
        if content_type == 'TEXT':
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_TIKTOK_TEXT_UNSUPPORTED,
                )
            )
            continue
        if not account.tiktok_prerequisites_met:
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_TIKTOK_PREREQS,
                    requires_action=True,
                    action_hint=ACTION_TIKTOK_PREREQS,
                )
            )
            continue
        if content_type == 'PHOTO' and not account.tiktok_photo_post_enabled:
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_TIKTOK_PHOTO_DISABLED,
                    requires_action=True,
                    action_hint=ACTION_TIKTOK_PHOTO,
                )
            )
            continue
        account_availabilities.append(
            AccountAvailability(
                social_account_id=account.id,
                display_name=account.display_name,
                available=True,
                reason=None,
            )
        )
    default_reason = REASON_NO_ACCOUNT if not accounts else REASON_TIKTOK_PREREQS
    return _platform_from_accounts(Platform.TIKTOK.value, account_availabilities, default_reason)


def _evaluate_youtube(accounts, content_type):
    account_availabilities = []
    for account in accounts:
        if content_type != 'VIDEO':
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_YT_VIDEO_ONLY,
                )
            )
            continue
        account_availabilities.append(
            AccountAvailability(
                social_account_id=account.id,
                display_name=account.display_name,
                available=True,
                reason=None,
            )
        )
    if content_type != 'VIDEO':
        default_reason = REASON_YT_VIDEO_ONLY
    else:
        default_reason = REASON_NO_ACCOUNT if not accounts else REASON_YT_VIDEO_ONLY
    return _platform_from_accounts(Platform.YOUTUBE.value, account_availabilities, default_reason)


def _evaluate_linkedin(accounts, content_type):
    account_availabilities = []
    for account in accounts:
        if not account.linkedin_access_granted:
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_LINKEDIN_SCOPE,
                    requires_action=True,
                    action_hint=ACTION_LINKEDIN,
                )
            )
            continue
        account_availabilities.append(
            AccountAvailability(
                social_account_id=account.id,
                display_name=account.display_name,
                available=True,
                reason=None,
            )
        )
    default_reason = REASON_NO_ACCOUNT if not accounts else REASON_LINKEDIN_SCOPE
    return _platform_from_accounts(Platform.LINKEDIN.value, account_availabilities, default_reason)


def _evaluate_x(accounts, content_type):
    account_availabilities = []
    for account in accounts:
        if content_type == 'TEXT':
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=True,
                    reason=None,
                )
            )
            continue
        if not account.x_media_upload_enabled:
            account_availabilities.append(
                AccountAvailability(
                    social_account_id=account.id,
                    display_name=account.display_name,
                    available=False,
                    reason=REASON_X_MEDIA_DISABLED,
                    requires_action=True,
                    action_hint=ACTION_X_MEDIA,
                )
            )
            continue
        account_availabilities.append(
            AccountAvailability(
                social_account_id=account.id,
                display_name=account.display_name,
                available=True,
                reason=None,
            )
        )
    default_reason = REASON_NO_ACCOUNT if not accounts else REASON_X_MEDIA_DISABLED
    return _platform_from_accounts(Platform.X.value, account_availabilities, default_reason)
