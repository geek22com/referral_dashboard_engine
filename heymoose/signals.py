# -*- coding: utf-8 -*-
from blinker import Namespace


_signals = Namespace()


user_blocked = _signals.signal('user-blocked')
confirmation_email_requested = _signals.signal('confirmation-email-requested')
password_restore_requested = _signals.signal('password-restore-requested')
contacts_list_add_failed = _signals.signal('contacts-list-add-failed')
new_feedback = _signals.signal('new-feedback')

offer_blocked = _signals.signal('offer-blocked')
offer_unblocked = _signals.signal('offer-unblocked')

site_moderated = _signals.signal('site-moderated')
placement_moderated = _signals.signal('placement-moderated')