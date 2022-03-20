import warnings
warnings.filterwarnings("ignore")
import csv

from app.controller.mrc_controller import MRC


if __name__ == "__main__":

    # 고려, 고구려, 조선, 고조선, 신라에 대해서 구분
    # title = "고구려"
    # for i in WikiControl().get_wiki_data(title):
    #     print(i)

    # ElasticContent().create(WikiQuestionItemDTO(title=title, question=None))
    # ElasticContent().create(WikiQuestionItemDTO(title="고구려", question=None))
    # ElasticContent().create(WikiQuestionItemDTO(title="조선", question=None))
    # ElasticContent().create(WikiQuestionItemDTO(title="고조선", question=None))

    mrc = MRC()

    spliter = " @@@ "

    answer = []
    with open("test_data/question.txt", "r", encoding='utf-8-sig') as file:
        # "\n표시 없이 데이터를 한줄씩 리스트로 읽음"
        sample = file.read().splitlines()
        for sample_item in sample:
            print(sample_item)
            mrc_answer, best_proper_content = mrc.filter_mrc_content(sample_item)
            print(mrc_answer, best_proper_content)

            answer.append([sample_item,str(mrc_answer) + " ",str(best_proper_content)])


    with open('test_data/answer.csv', 'a', encoding='utf-8-sig', newline='') as writer_csv:

        # 2. opewn writer
        writer = csv.writer(writer_csv, delimiter=',')

        for answer_item in answer:
            writer.writerow([*answer_item])
