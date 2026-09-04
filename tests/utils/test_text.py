from utils.text import contains_word, parse_word_filters


sample_message =  """
Chat: TECH DEALS EXCLUSIVE
Text: 🎧 Sony WH-1000XM5 Wireless Noise-Canceling Headphones

🔥 Price: $348.00 with discount
💳 Or $398.00 in 6x interest-free installments

🛒 Purchase Link 👇
https://techdeals.com/item/84920

    Category: !(Audio Electronics),   15% OFF,
 
Sold by Amazon.
Link: https://t.me/techdeals_official/98412
"""



def test_contains_word():
    assert contains_word("$398.00", sample_message) is True
    assert contains_word("398.00", sample_message) is True
    assert contains_word("Category", sample_message) is True
    assert contains_word("15", sample_message) is False
    assert contains_word("15%", sample_message) is True
    assert contains_word("15% OFF", sample_message) is True
    assert contains_word("Audio Electronics", sample_message) is True
    assert contains_word("Audio  Electronics", sample_message) is False # extra space
    assert contains_word("Sold by Amazon", sample_message) is True
    assert contains_word("amazon", sample_message) is True
    assert contains_word("https://techdeals.com/item/84920", sample_message) is True
    assert contains_word("interest-free", sample_message) is True
    assert contains_word("Cancel", sample_message) is False
    assert contains_word("Head", sample_message) is False
    assert contains_word("install", sample_message) is False
    assert contains_word("interest", sample_message) is False


def test_parse_word_filters():
    assert parse_word_filters(" product 1 ")[0].get_value() == ['product 1']
    assert len(parse_word_filters("product 1; product 2; product 3")) == 3
    assert len(parse_word_filters("product 1; product 2; product 3 + discount")) == 3
    assert parse_word_filters("product 1; product 2; product 3 + discount")[2].get_value() == ["product 3", "discount"]