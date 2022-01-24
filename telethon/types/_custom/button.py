import typing

from .messagebutton import MessageButton
from ... import _tl
from ..._misc import utils, hints


class Button:
    """
    .. note::

        This class is used to **define** reply markups, e.g. when
        sending a message or replying to events. When you access
        `Message.buttons <telethon.tl.custom.message.Message.buttons>`
        they are actually `MessageButton
        <telethon.tl.custom.messagebutton.MessageButton>`,
        so you might want to refer to that class instead.

    Helper class to allow defining ``reply_markup`` when
    sending a message with inline or keyboard buttons.

    You should make use of the defined class methods to create button
    instances instead making them yourself (i.e. don't do ``Button(...)``
    but instead use methods line `Button.inline(...) <inline>` etc.

    You can use `inline`, `switch_inline`, `url`, `auth`, `buy` and `game`
    together to create inline buttons (under the message).

    You can use `text`, `request_location`, `request_phone` and `request_poll`
    together to create a reply markup (replaces the user keyboard).
    You can also configure the aspect of the reply with these.
    The latest message with a reply markup will be the one shown to the user
    (messages contain the buttons, not the chat itself).

    You **cannot** mix the two type of buttons together,
    and it will error if you try to do so.

    The text for all buttons may be at most 142 characters.
    If more characters are given, Telegram will cut the text
    to 128 characters and add the ellipsis (…) character as
    the 129.
    """
    def __init__(self, button, *, resize, single_use, selective):
        self.button = button
        self.resize = resize
        self.single_use = single_use
        self.selective = selective

    @staticmethod
    def _is_inline(button):
        """
        Returns `True` if the button belongs to an inline keyboard.
        """
        return isinstance(button, (
            _tl.KeyboardButtonBuy,
            _tl.KeyboardButtonCallback,
            _tl.KeyboardButtonGame,
            _tl.KeyboardButtonSwitchInline,
            _tl.KeyboardButtonUserProfile,
            _tl.KeyboardButtonUrl,
            _tl.InputKeyboardButtonUrlAuth
        ))

    @staticmethod
    def inline(text, data=None):
        """
        Creates a new inline button with some payload data in it.

        If `data` is omitted, the given `text` will be used as `data`.
        In any case `data` should be either `bytes` or `str`.

        Note that the given `data` must be less or equal to 64 bytes.
        If more than 64 bytes are passed as data, ``ValueError`` is raised.
        If you need to store more than 64 bytes, consider saving the real
        data in a database and a reference to that data inside the button.

        When the user clicks this button, `events.CallbackQuery
        <telethon.events.callbackquery.CallbackQuery>` will trigger with the
        same data that the button contained, so that you can determine which
        button was pressed.
        """
        if not data:
            data = text.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray, memoryview)):
            data = str(data).encode('utf-8')

        if len(data) > 64:
            raise ValueError('Too many bytes for the data')

        return _tl.KeyboardButtonCallback(text, data)

    @staticmethod
    def switch_inline(text, query='', same_peer=False):
        """
        Creates a new inline button to switch to inline query.

        If `query` is given, it will be the default text to be used
        when making the inline query.

        If ``same_peer is True`` the inline query will directly be
        set under the currently opened chat. Otherwise, the user will
        have to select a different dialog to make the query.

        When the user clicks this button, after a chat is selected, their
        input field will be filled with the username of your bot followed
        by the query text, ready to make inline queries.
        """
        return _tl.KeyboardButtonSwitchInline(text, query, same_peer)

    @staticmethod
    def url(text, url=None):
        """
        Creates a new inline button to open the desired URL on click.

        If no `url` is given, the `text` will be used as said URL instead.

        You cannot detect that the user clicked this button directly.

        When the user clicks this button, a confirmation box will be shown
        to the user asking whether they want to open the displayed URL unless
        the domain is trusted, and once confirmed the URL will open in their
        device.
        """
        return _tl.KeyboardButtonUrl(text, url or text)

    @staticmethod
    def auth(text, url=None, *, bot=None, write_access=False, fwd_text=None):
        """
        Creates a new inline button to authorize the user at the given URL.

        You should set the `url` to be on the same domain as the one configured
        for the desired `bot` via `@BotFather <https://t.me/BotFather>`_ using
        the ``/setdomain`` command.

        For more information about letting the user login via Telegram to
        a certain domain, see https://core.telegram.org/widgets/login.

        If no `url` is specified, it will default to `text`.

        Args:
            bot (`hints.EntityLike`):
                The bot that requires this authorization. By default, this
                is the bot that is currently logged in (itself), although
                you may pass a different input peer.

                .. note::

                    For now, you cannot use ID or username for this argument.
                    If you want to use a different bot than the one currently
                    logged in, you must manually use `client.get_input_entity()
                    <telethon.client.users.UserMethods.get_input_entity>`.

            write_access (`bool`):
                Whether write access is required or not.
                This is `False` by default (read-only access).

            fwd_text (`str`):
                The new text to show in the button if the message is
                forwarded. By default, the button text will be the same.

        When the user clicks this button, a confirmation box will be shown
        to the user asking whether they want to login to the specified domain.
        """
        return _tl.InputKeyboardButtonUrlAuth(
            text=text,
            url=url or text,
            bot=utils.get_input_user(bot or _tl.InputUserSelf()),
            request_write_access=write_access,
            fwd_text=fwd_text
        )

    @staticmethod
    def mention(text, input_entity):
        """
        Creates a new inline button linked to the profile of user.

        Args:
            input_entity:
                Input entity of :tl:User to use for profile button.
                By default, this is the logged in user (itself), although
                you may pass a different input peer.

                .. note::

                    For now, you cannot use ID or username for this argument.
                    If you want to use different user, you must manually use
                    `client.get_input_entity() <telethon.client.users.UserMethods.get_input_entity>`.
        """
        return _tl.InputKeyboardButtonUserProfile(
            text,
            utils.get_input_user(input_entity or _tl.InputUserSelf())
        )


    @classmethod
    def text(cls, text, *, resize=None, single_use=None, selective=None):
        """
        Creates a new keyboard button with the given text.

        Args:
            resize (`bool`):
                If present, the entire keyboard will be reconfigured to
                be resized and be smaller if there are not many buttons.

            single_use (`bool`):
                If present, the entire keyboard will be reconfigured to
                be usable only once before it hides itself.

            selective (`bool`):
                If present, the entire keyboard will be reconfigured to
                be "selective". The keyboard will be shown only to specific
                users. It will target users that are @mentioned in the text
                of the message or to the sender of the message you reply to.

        When the user clicks this button, a text message with the same text
        as the button will be sent, and can be handled with `events.NewMessage
        <telethon.events.newmessage.NewMessage>`. You cannot distinguish
        between a button press and the user typing and sending exactly the
        same text on their own.
        """
        return cls(_tl.KeyboardButton(text),
                   resize=resize, single_use=single_use, selective=selective)

    @classmethod
    def request_location(cls, text, *,
                         resize=None, single_use=None, selective=None):
        """
        Creates a new keyboard button to request the user's location on click.

        ``resize``, ``single_use`` and ``selective`` are documented in `text`.

        When the user clicks this button, a confirmation box will be shown
        to the user asking whether they want to share their location with the
        bot, and if confirmed a message with geo media will be sent.
        """
        return cls(_tl.KeyboardButtonRequestGeoLocation(text),
                   resize=resize, single_use=single_use, selective=selective)

    @classmethod
    def request_phone(cls, text, *,
                      resize=None, single_use=None, selective=None):
        """
        Creates a new keyboard button to request the user's phone on click.

        ``resize``, ``single_use`` and ``selective`` are documented in `text`.

        When the user clicks this button, a confirmation box will be shown
        to the user asking whether they want to share their phone with the
        bot, and if confirmed a message with contact media will be sent.
        """
        return cls(_tl.KeyboardButtonRequestPhone(text),
                   resize=resize, single_use=single_use, selective=selective)

    @classmethod
    def request_poll(cls, text, *, force_quiz=False,
                     resize=None, single_use=None, selective=None):
        """
        Creates a new keyboard button to request the user to create a poll.

        If `force_quiz` is `False`, the user will be allowed to choose whether
        they want their poll to be a quiz or not. Otherwise, the user will be
        forced to create a quiz when creating the poll.

        If a poll is a quiz, there will be only one answer that is valid, and
        the votes cannot be retracted. Otherwise, users can vote and retract
        the vote, and the pol might be multiple choice.

        ``resize``, ``single_use`` and ``selective`` are documented in `text`.

        When the user clicks this button, a screen letting the user create a
        poll will be shown, and if they do create one, the poll will be sent.
        """
        return cls(_tl.KeyboardButtonRequestPoll(text, quiz=force_quiz),
                   resize=resize, single_use=single_use, selective=selective)

    @staticmethod
    def clear(selective=None):
        """
        Clears all keyboard buttons after sending a message with this markup.
        When used, no other button should be present or it will be ignored.

       ``selective`` is as documented in `text`.

        """
        return _tl.ReplyKeyboardHide(selective=selective)

    @staticmethod
    def force_reply(single_use=None, selective=None, placeholder=None):
        """
        Forces a reply to the message with this markup. If used,
        no other button should be present or it will be ignored.

        ``single_use`` and ``selective`` are as documented in `text`.

        Args:
            placeholder (str):
                text to show the user at typing place of message.

                If the placeholder is too long, Telegram applications will
                crop the text (for example, to 64 characters and adding an
                ellipsis (…) character as the 65th).
        """
        return _tl.ReplyKeyboardForceReply(
            single_use=single_use,
            selective=selective,
            placeholder=placeholder)

    @staticmethod
    def buy(text):
        """
        Creates a new inline button to buy a product.

        This can only be used when sending files of type
        :tl:`InputMediaInvoice`, and must be the first button.

        If the button is not specified, Telegram will automatically
        add the button to the message. See the
        `Payments API <https://core.telegram.org/api/payments>`__
        documentation for more information.
        """
        return _tl.KeyboardButtonBuy(text)

    @staticmethod
    def game(text):
        """
        Creates a new inline button to start playing a game.

        This should be used when sending files of type
        :tl:`InputMediaGame`, and must be the first button.

        See the
        `Games <https://core.telegram.org/api/bots/games>`__
        documentation for more information on using games.
        """
        return _tl.KeyboardButtonGame(text)


def build_reply_markup(
        buttons: 'typing.Optional[hints.MarkupLike]',
        inline_only: bool = False) -> 'typing.Optional[_tl.TypeReplyMarkup]':
    """
    Builds a :tl:`ReplyInlineMarkup` or :tl:`ReplyKeyboardMarkup` for
    the given buttons.

    Does nothing if either no buttons are provided or the provided
    argument is already a reply markup.

    You should consider using this method if you are going to reuse
    the markup very often. Otherwise, it is not necessary.

    This method is **not** asynchronous (don't use ``await`` on it).

    Arguments
        buttons (`hints.MarkupLike`):
            The button, list of buttons, array of buttons or markup
            to convert into a markup.

        inline_only (`bool`, optional):
            Whether the buttons **must** be inline buttons only or not.
    """
    if not buttons:
        return None

    try:
        if buttons.SUBCLASS_OF_ID == 0xe2e10ef2:
            return buttons  # crc32(b'ReplyMarkup'):
    except AttributeError:
        pass

    if not utils.is_list_like(buttons):
        buttons = [buttons]
    if not utils.is_list_like(buttons[0]):
        buttons = [[b] for b in buttons]

    is_inline = False
    is_normal = False
    resize = None
    single_use = None
    selective = None

    rows = []
    for row in buttons:
        current = []
        for button in row:
            if isinstance(button, Button):
                if button.resize is not None:
                    resize = button.resize
                if button.single_use is not None:
                    single_use = button.single_use
                if button.selective is not None:
                    selective = button.selective

                button = button.button
            elif isinstance(button, MessageButton):
                button = button.button

            inline = Button._is_inline(button)
            is_inline |= inline
            is_normal |= not inline

            if button.SUBCLASS_OF_ID == 0xbad74a3:
                # 0xbad74a3 == crc32(b'KeyboardButton')
                current.append(button)

        if current:
            rows.append(_tl.KeyboardButtonRow(current))

    if inline_only and is_normal:
        raise ValueError('You cannot use non-inline buttons here')
    elif is_inline == is_normal and is_normal:
        raise ValueError('You cannot mix inline with normal buttons')
    elif is_inline:
        return _tl.ReplyInlineMarkup(rows)
    # elif is_normal:
    return _tl.ReplyKeyboardMarkup(
        rows, resize=resize, single_use=single_use, selective=selective)