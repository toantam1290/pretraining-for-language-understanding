import argparse
import pickle
from tokenization import Vocab, Tokenizer

def argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--corpus', required=True)
    p.add_argument('--vocab', required=True)
    p.add_argument('--is_tokenized', action='store_true')
    p.add_argument('--tokenizer', default='mecab')
    p.add_argument('--unk_token', default='<unk>', type=str,
                   help='The representation for any unknown token')
    p.add_argument('--pad_token', default='<pad>', type=str,
                   help='The representation for the special token of padding token')
    p.add_argument('--bos_token', default='<bos>', type=str,
                   help='The representation for the special token of beginning-of-sequence token')
    p.add_argument('--eos_token', default='<eos>', type=str,
                   help='The representation for the special token of end-of-sequence token')
    p.add_argument('--min_freq', default=3, type=int,
                   help='The minimum frequency required for a token')
    p.add_argument('--lower', action='store_true',
                   help='Whether to convert the texts to lowercase')

    config = p.parse_args()
    return config

def main(config):
    print(config)
    
    list_of_tokens = []
    if config.is_tokenized:
        # read tokens
        with open(config.corpus, 'r', encoding='utf8') as reader:
            for li, line in enumerate(reader):
                list_of_tokens += line.strip().split()
    else:
        # select tokenizer
        if config.tokenizer=='mecab':
            from konlpy.tag import Mecab
            tokenizer = Tokenizer(tokenization_fn=Mecab().morphs)

        # tokenization & read tokens
        with open(config.corpus, 'r', encoding='utf8') as reader:
            for li, line in enumerate(reader):
                list_of_tokens += tokenizer.tokenize(line.strip())

    # build vocabulary                
    vocab = Vocab(list_of_tokens=list_of_tokens,
                  unk_token=config.unk_token,
                  pad_token=config.pad_token,
                  bos_token=config.bos_token,
                  eos_token=config.eos_token,
                  min_freq=config.min_freq,
                  lower=config.lower)
    vocab.build()
    print('Vocabulary size: ', len(vocab))

    # save vocabulary
    with open(config.vocab, 'wb') as writer:
        pickle.dump(vocab, writer)
    print('Vocabulary saved to', config.vocab)

if __name__=='__main__':
    config = argparser()
    main(config)