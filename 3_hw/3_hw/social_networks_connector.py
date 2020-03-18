import requests

VK_IS_ACTIVE = False
TWITTER_IS_ACTIVE = False


class SocialNetworksConnector:
    class ConfigVK:
        # VK_APP_ID = '7356833'
        # VK_PROTECTED_KEY = 'rDAhO46PSTcUbtS1rTUd'
        VK_SERVICE_ACCESS_KEY = '1fddcb421fddcb421fddcb42fc1fad8ae311fdd1fddcb4241b6baa92fd1dc1eecb445c3'
        ACCESS_TOKEN = 'e9d323b8d7d23e1a0f476a1af4f23f4815dbf7017b5eb13fca4ca03b8c216c84307c5739d4838372ccfe0'
        API_VERSION = '5.103'

        USER_INFO_PARAMETERS = ['photo_id',
                                'verified',
                                'sex',
                                'bdate',
                                'city',
                                'country',
                                'home_town',
                                'has_photo',
                                'photo_50',
                                'photo_100',
                                'photo_200_orig',
                                'photo_200',
                                'photo_400_orig',
                                'photo_max',
                                'photo_max_orig',
                                'online',
                                'domain',
                                'has_mobile',
                                'contacts',
                                'site',
                                'education',
                                'universities',
                                'schools',
                                'status',
                                'last_seen',
                                'followers_count',
                                'common_count',
                                'occupation',
                                'nickname',
                                'relatives',
                                'relation',
                                'personal',
                                'connections',
                                'exports',
                                'activities',
                                'interests',
                                'music',
                                'movies',
                                'tv',
                                'books',
                                'games',
                                'about',
                                'quotes',
                                'can_post',
                                'can_see_all_posts',
                                'can_see_audio',
                                'can_write_private_message',
                                'can_send_friend_request',
                                'is_favorite',
                                'is_hidden_from_feed',
                                'timezone',
                                'screen_name',
                                'maiden_name',
                                'crop_photo',
                                'is_friend',
                                'friend_status',
                                'career',
                                'military',
                                'blacklisted',
                                'blacklisted_by_me',
                                'can_be_invited_group']

    def __init__(self, social_net='vk'):
        clear_social_net = social_net.strip().lower()
        if clear_social_net == 'vk':
            self.social_net = 'vk'
            global VK_IS_ACTIVE
            if VK_IS_ACTIVE:
                raise ConnectionError("VK is already connected")
            VK_IS_ACTIVE = True
        elif clear_social_net == 'twitter':
            self.social_net == 'twitter'
            global TWITTER_IS_ACTIVE
            if TWITTER_IS_ACTIVE:
                raise ConnectionError("Twitter is already connected")
            TWITTER_IS_ACTIVE = True

    def get_user_profile(self, some_user):
        get_profile_url = f'''https://api.vk.com/method/users.get?user_ids={some_user}&v={self.ConfigVK.API_VERSION}&fields={f"{','.join(self.ConfigVK.USER_INFO_PARAMETERS)}&"}access_token={self.ConfigVK.ACCESS_TOKEN}'''
        response = requests.get(get_profile_url).json()
        if 'error' in response:
            raise Exception(f"{response['error']['error_msg']}")
        # if response.status_code == 18:
        #     raise Exception("The page was deleted or banned")
        # elif response.status_code == 19:
        #     raise Exception("Content is unavailable")
        # elif response.status_code == 30:
        #     raise Exception("Profile is private")

        return response

    def get_user_followers_profile(self, some_user):
        get_followers_profile_url = f'''https://api.vk.com/method/users.getFollowers?user_ids={some_user}&v={self.ConfigVK.API_VERSION}&fields={f"{','.join(self.ConfigVK.USER_INFO_PARAMETERS)}&"}access_token={self.ConfigVK.ACCESS_TOKEN}'''
        response = requests.get(get_followers_profile_url).json()
        if 'error' in response:
            raise Exception(f"{response['error']['error_msg']}")
        return get_followers_profile_url

    def get_wall_records(self, some_user):
        get_wall_url = f'''https://api.vk.com/method/wall.get?owner_id={some_user}&extended=1&v={self.ConfigVK.API_VERSION}&fields={f"{','.join(self.ConfigVK.USER_INFO_PARAMETERS)}&"}access_token={self.ConfigVK.ACCESS_TOKEN}'''
        if type(some_user) == str:
            get_wall_url = get_wall_url.replace('owner_id', 'domain')
        response = requests.get(get_wall_url).json()
        if 'error' in response:
            raise Exception(f"{response['error']['error_msg']}")
        return get_wall_url

    def __del__(self):
        if self.social_net == 'vk':
            global VK_IS_ACTIVE
            VK_IS_ACTIVE = False
        elif self.social_net == 'twitter':
            global TWITTER_IS_ACTIVE
            TWITTER_IS_ACTIVE = False


if __name__ == '__main__':
    A = SocialNetworksConnector()
    r = A.get_user_profile(some_user=34534)
    print(r)
    f = A.get_user_followers_profile(some_user=144519634)
    l2 = A.get_user_profile(some_user='idi13i10i')
    f2 = A.get_user_followers_profile(some_user='idi13i10i')
    l3 = A.get_wall_records(some_user=144519634)
    f3 = A.get_wall_records(some_user='idi13i10i')
    print(l2)
    print(f2)
    print(l3)
    print(f3)
