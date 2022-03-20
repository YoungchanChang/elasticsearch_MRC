from app.controller.mrc_controller import MRC


def test_mrc():
    mrc = MRC()
    result = mrc.get_elastic_content("조선시대 최고 학부는 어디야")
    assert result == ('성균관', (14, 16))