import sconce
import sys
from model import *
from sklearn.decomposition import PCA
hidden_size = 256
embed_size = 50
learning_rate = 0.0001
n_epochs = 100000
grad_clip = 1.0

kld_start_inc = 10000
kld_weight = 0.05
kld_max = 0.1
kld_inc = 0.000002
temperature = 0.9
temperature_min = 0.5
temperature_dec = 0.000002
# Training
# ------------------------------------------------------------------------------

with open('data/tyc.txt', 'r', encoding='utf-8') as f:
    tyc_data = f.readlines()
with open('data/20000_law.json', 'r', encoding='utf-8') as f:
    law_data = f.readlines()
with open('data/20000_other_law.json', 'r', encoding='utf-8') as f:
    law_other_data = f.readlines()
tyc_list = []
for data in tyc_data:
    tyc_list.append(data.split('\n')[0])

file_len = 0
lines = []
for data in law_data:
    file_len += len(data.split('\n')[0])
    lines.append(data.split('\n')[0])
for data in law_other_data:
    file_len += len(data.split('\n')[0])
    lines.append(data.split('\n')[0])
def good_size(line):
    return len(line) >= MIN_LENGTH and len(line) <= MAX_LENGTH
def good_content(line):
    return 'http' not in line and '/' not in line

lines = [line for line in lines if good_size(line) and good_content(line)]

random.shuffle(lines) #用于将一个列表中的元素打乱
print('开始对文档进行分词')
doc_words = [" ".join(jieba.cut(sent0)) for sent0 in lines]# 使用jieba对每个文档进行分词
print('分词完成，开始就对文档进行fit')
tfidf_model = TfidfVectorizer(token_pattern=r"(?u)\b\w\w+\b",max_df=0.8,min_df=5, stop_words=tyc_list).fit(doc_words)
lawvocab = tfidf_model.vocabulary_ # 得到词表
n_characters = len(lawvocab) # 得到词表长度
print('fit结束，得到词表，开始对数据进行分块')
# 对数据集进行分块，用于分批进行TF-IDF计算，生成稀疏矩阵
law_Blockdata = [lines[i:i + 5000] for i in range(0, len(lines), 5000)]
print('分块完成，开始初始化模型')
#encode层：n_characters表示字符串词表大小
e = EncoderRNN(512, hidden_size, embed_size)
d = DecoderRNN(embed_size, hidden_size, 512, 2)
vae = VAE(e, d)
optimizer = torch.optim.Adam(vae.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()
if USE_CUDA:
    vae.cuda()
    criterion.cuda()
log_every = 200
save_every = 5000
# job = sconce.Job('vae', {
#     'hidden_size': hidden_size,
#     'embed_size': embed_size,
#     'learning_rate': learning_rate,
#     'kld_weight': kld_weight,
#     'temperature': temperature,
#     'grad_clip': grad_clip
# })
# job.log_every = log_every

def save():
    save_filename = 'vae.pt'
    torch.save(vae, save_filename)
    print('Saved as %s' % save_filename)
print('模型初始化完成，现在开始训练')
pca = PCA(n_components=512,svd_solver='randomized', copy=True, random_state=8)
try:
    for epoch in range(n_epochs):
        for blockdata in law_Blockdata:
            print('开始第{}批次，共{}块数据'.format(epoch,len(law_Blockdata)))
            tfidf_list = tfidf_model.transform(blockdata).toarray() # 使用tfidf实例得到文档表征。
            pac_list = pca.fit_transform(tfidf_list)
            # input = random.choice(tfidf_list) # 从序列中随机选取一个元素
            for input in pac_list:
                tentor_input = torch.Tensor(input).float()
                target = input.copy()
                tentor_target = torch.Tensor(target).float()
                optimizer.zero_grad()

                m, l, z, decoded = vae(tentor_input, temperature)
                if temperature > temperature_min:
                    temperature -= temperature_dec

                loss = criterion(decoded, tentor_target)
                # job.record(epoch, loss.data[0])

                KLD = (-0.5 * torch.sum(l - torch.pow(m, 2) - torch.exp(l) + 1, 1)).mean().squeeze()
                loss += KLD * kld_weight

                if epoch > kld_start_inc and kld_weight < kld_max:
                    kld_weight += kld_inc
                optimizer.zero_grad()
                loss.backward()
                # print('from', next(vae.parameters()).grad.data[0][0])
                ec = torch.nn.utils.clip_grad_norm_(vae.parameters(), grad_clip)
                # print('to  ', next(vae.parameters()).grad.data[0][0])
                optimizer.step()
                print('结束')
        if epoch % log_every == 0:
            print('[%d] %.4f (k=%.4f, t=%.4f, kl=%.4f, ec=%.4f)' % (
                epoch, loss.item(), kld_weight, temperature, KLD.item(), ec
            ))
            print('(target) "%s"' % longtensor_to_string(tentor_target))
            generated = vae.decoder.generate(z, MAX_LENGTH, temperature)
            print('(generated) "%s"' % tensor_to_string(generated))
            print('')

        if epoch > 0 and epoch % save_every == 0:
            save()

    save()

except KeyboardInterrupt as err:
    print("ERROR", err)
    print("Saving before quit...")
    save()

