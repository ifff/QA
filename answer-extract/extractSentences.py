# -*- coding: utf-8 -*-
import codecs
import re
import jieba
import jieba.posseg as pseg
from gensim import corpora, models, similarities

jieba.load_userdict('/home/fanff/QA/preprocess/userdict.txt')

#for i in xrange(1,15001):
for i in xrange(26,300,100):
    # Fetch top 3 docs
    paras = []
    for j in xrange(1,4):
        para_file = codecs.open( \
            ('/home/fanff/QA/IR/result/close/%d/%d') % (i, j), 'r', encoding='utf-8')
        paras.append(para_file.read().splitlines()[1:])
        para_file.close()
    #sents = [para.split(u'。') for para in sum(paras, [])]
    sents = [re.split(u'。|；', para) for para in sum(paras, [])]
    sents = sum(sents, [])
    pos_sents = [pseg.cut(sent) for sent in sents]
    pos_sents = [[word for word in sent] for sent in pos_sents]
    split_sents = [[word.word for word in sent] for sent in pos_sents]
    #split_sents = [[word for word in sent] for sent in split_sents]
    query_file = codecs.open('/home/fanff/QA/segment/query/%d.seg' \
                             % i, 'r', encoding='utf-8')
    query = query_file.read().splitlines()
    query_file.close()
    query = query[0].split(' ')  
    '''
    dic = corpora.Dictionary(split_sents)
    corpus = [dic.doc2bow(sent) for sent in split_sents]

    query_bow = dic.doc2bow(query)

    #index = similarities.SparseMatrixSimilarity(corpus, num_features=len(dic))
    #sims = index[query_bow]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    query_tfidf = tfidf[query_bow]
    index = similarities.SparseMatrixSimilarity(corpus_tfidf, \
                                                num_features=len(dic))
    sims = index[query_tfidf]
    sims = sorted(enumerate(sims), key=lambda item: -item[-1])
    '''
    sims = []
    for sent in split_sents:
        new_sents = [sent, query]
        dic = corpora.Dictionary(new_sents)
        corpus = [dic.doc2bow(sent) for sent in new_sents]
        query_bow = dic.doc2bow(query)
        index = similarities.SparseMatrixSimilarity(corpus, num_features=len(dic))
        sim = index[query_bow]
        sims.append(sim[0])

    k = 3
    if len(sims) < 3:
        k = 0
    
    print sims[0:k]
    print ' '.join([str(item[0]) + '/' + str(item[1]) for item in sims[0:k]])
    topk_sents = [sents[item[0]] for item in sims[0:k]]
    fi = codecs.open('/home/fanff/QA/answer-extract/candidate/close/%d.raw' \
                     % i, 'w', encoding='utf-8')
    fi.write('\n'.join(topk_sents))
    fi.close()

    topk_split_sents = [split_sents[item[0]] for item in sims[0:k]]
    fi = codecs.open('/home/fanff/QA/answer-extract/candidate/close/%d.seg' \
                     % i, 'w', encoding='utf-8')
    fi.write('\n'.join([' '.join(sent) for sent in topk_split_sents]))
    fi.close()
 
    topk_pos_sents = [pos_sents[item[0]] for item in sims[0:k]]
    fi = codecs.open('/home/fanff/QA/answer-extract/candidate/close/%d.pos' \
                     % i, 'w', encoding='utf-8')
    fi.write('\n'.join(['\t'.join([word.word + ' ' + word.flag \
                                   for word in sent]) \
                        for sent in topk_pos_sents]))
    fi.close()
