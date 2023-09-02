.. image:: https://fs.noorgram.ir/xen/2020/12/941_ca20211dfe5a29ee7916f6a87df17e69_thumb.jpg
    :target: https://ble.ir/belix_py
    :alt: Logo Bale


Library INFO
=============

Bale Info:

* `Creator ID in Bale <https://ble.ir/user_xcoder>`_
* `Bale Channel <https://ble.ir/belix_py>`_

Subscribe to the channels to know about the library and sources updates.

Installing BeliX from PyPI
=================================

.. code-block:: python3

    pip install BeliX

If you have a problem with the installation, subscribe to the channel.

How to import the BeliX
===============================

.. code-block:: python3

    from BeliX import Bale

    bot = Bale('token')

Quick start
===========

.. code-block:: python3

    from BeliX import Bale,color
    
    bot = Bale('token')

    for msg in bot.getChatUpdate():
        print(f'{color.green}Message {color.blue}>> {color.white}{msg.text}')
        if msg.text == 'hello':
            bot.sendMessage(msg.chat_id,'hello world',reply_message_id=msg.message_id)
