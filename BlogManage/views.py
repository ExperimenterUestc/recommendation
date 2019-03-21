# coding=utf-8
import re
import pandas
import numpy
import random
from django.shortcuts import render
from BlogManage.models import UserFilmRank, Film
from BlogManage.forms import RankForm, nameForm
from UserManage.models import User
from django.contrib.auth.decorators import login_required
from UserManage.views.permission import PermissionVerify
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response,RequestContext,redirect
from website.common.CommonPaginator import SelfPaginator
# -*- coding: utf-8 -*-
@login_required
def FilmSearch(request):
    if request.method == 'POST':
        form = nameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name1']
            film_search = Filmfinder(name)

        form_next = RankForm()
        kwvars = {
                'form_next': form_next,
                'request': request,
                'ans': film_search
            }
        return render_to_response('FilmManage/film.write.html', kwvars, RequestContext(request))
    else:
        return render(request, 'FilmManage/film.search.html')


@login_required
# @PermissionVerify()
def WriteRank(request):
    if request.method == "POST":
        article = UserFilmRank()
        article.author = request.user
        form = RankForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('film_read', kwargs={'username':request.user.username}))
    else:
        form = RankForm()

    kwvars = {
        'form': form,
        'request': request,
    }
    return render_to_response('FilmManage/film.write.html', kwvars, RequestContext(request))


# @login_required
# @PermissionVerify()
def ReadUserRank(request, username):
    author_list = User.objects.filter(username=username)
    if(len(author_list)!=1):
        return render_to_response("Not a useful adress.")
    rank_list = UserFilmRank.objects.order_by('mod_date').filter(author=author_list[0])[::-1]
    # rank_list = UserFilmRank.objects.filter(author=author_list[0])
    temp_l = UserFilmRank.objects.filter(author=author_list[0])
    film_list = Film.objects.all()
    l = []
    for i in temp_l:
        for ii in film_list:
            if i.name == ii.title:
                l.append((ii.movieid, ii.title, ii.genres))
    # lst = SelfPaginator(request, rank_list, 20)
    kwvars = {
        # 'lPage': lst,
        'request': request,
        'rank_list': rank_list,
        'rank_film': l,
        'author': author_list[0]
    }
    return render_to_response('FilmManage/film.read.html', kwvars, RequestContext(request))


def PublicFilm(request):
    import random
    film_list = Film.objects.all()
    if(len(film_list)>50):
        film_list = random.sample(film_list, 50)
    kwvars = {
        # 'lPage': lst,
        'request': request,
        'film_list': film_list,
    }
    return render_to_response("FilmManage/film.public.html", kwvars, RequestContext(request))


@login_required
def ManageRank(request):
    if(request.method=="GET"):
        article_list = UserFilmRank.objects.order_by('mod_date').filter(author=request.user)[::-1]
        kwvars = {
            'request': request,
            'article_list': article_list,
        }
        return render_to_response('FilmManage/film.manage.html', kwvars, RequestContext(request))
    else:
        article_id = request.POST['article_id']
        a = UserFilmRank.objects.get(id=article_id)
        if(a.author==request.user):
            a.delete()
        return redirect('film_manage')

pop_f = [(356, 341), (296, 324), (318, 311), (593, 304), (260, 291), (480, 274), (2571, 259), (1, 247), (527, 243), (589, 237), (1196, 233), (110, 227), (1270, 226), (608, 223), (1198, 220), (2858, 220), (780, 218), (1210, 217), (588, 215), (457, 213), (590, 202), (47, 201), (50, 201), (150, 200), (364, 200), (2959, 200), (4993, 200), (380, 198), (32, 196), (858, 196)]
pop = [356, 296, 318, 593, 260,  480, 2571, 1, 527,589,1196, 110,1270, 608, 1198,2858, 780, 1210,588, 457, 590,47,50, 150,364, 2959,4993, 380, 32, 858]

@login_required
def Recommend(request):
    film_n = UserFilmRank.objects.filter(author=request.user.id)
    film_list = Film.objects.all()
    part_p = random.sample(pop_f, 8)
    l_p = []
    for i in part_p:
        for ii in film_list:
            if int(i[0]) == ii.movieid:
                l_p.append((ii.movieid, ii.title, ii.genres, i[1]))
    if len(film_n) == 0:
        kwvars = {
            # 'lPage': lst,
            'request': request,
            'list_p': l_p,
            'author': request.user
        }
        return render_to_response('FilmManage/film.firstrec.html', kwvars, RequestContext(request))

    elif len(film_n)!=0:
        sim_id = user_cf(film_n)
        kind_u = user_kind(film_n)
        final_m = item_cf(sim_id, film_n, kind_u)

        l = []
        for i in final_m:
            for ii in film_list:
                if int(i[0]) == ii.movieid:
                    if len(ii.imdbId)==5:
                        ii.imdbId = '00' + ii.imdbId
                    if len(ii.imdbId)==6:
                        ii.imdbId = '0' + ii.imdbId
                    l.append((ii.movieid, ii.title, ii.genres, ii.imdbId))

        kwvars = {
            # 'lPage': lst,
            'request': request,
            'list': l,
            'list_p': l_p[0:4],
            'author': request.user
        }
        return render_to_response('FilmManage/film.recommend.html', kwvars, RequestContext(request))

file_rate = pandas.read_csv("user_average0515.csv", names=['user_id', 'average', 'movie_all', 'point_all'])
m_f = pandas.read_csv("movies.csv", names=['movieId', 'title', 'genres', 'average', 'account'], nrows=9126)


def user_cf(user_rank):
    # 基于用户的协同过滤
    # 先求个用户的平均分
    temp_a = 0.0
    for i in user_rank:
        temp_a = temp_a + float(i.text)
    temp_a = temp_a / len(user_rank)

    # 用tittle去匹配找到对应的电影id
    film_list = Film.objects.all()
    l_u_mid = []
    for i in user_rank:
        for ii in film_list:
            if i.name == ii.title:
                l_u_mid.append(ii.movieid)

    sim = 0.0
    temp_sim = 0
    final_id = 0

    for i in range(len(file_rate)):
        l_temp_f = file_rate.movie_all[i]
        l_temp_p = file_rate.point_all[i]
        #得到每一个比对数据的电影列表,然后进行数据读取,在得到一个对应的评分列表
        l_temp_f = l_temp_f.strip('[]').split(',')
        l_temp_p = l_temp_p.strip('[]').split(',')

        for ii in range(len(l_temp_f)):
            for iii in range(len(user_rank)):
                if int(l_u_mid[iii]) == int(l_temp_f[ii]):
                    # 进行电影数据对比，加入喜好元素
                    # 平均值差值的乘积来判定是否喜好一致，同正或同负
                    # 改进：有的人看的电影太多，就是说他看的太全面可能和很多人都相似
                    if (float(user_rank[iii].text) - temp_a) * (float(l_temp_p[ii]) - float(file_rate.average[i])) >= 0.0:
                        sim = sim + 1
                    else:
                        sim = sim - 1
        # 对电影数量比值做一个权重，电影看得多的人也有推荐价值，不过要打个折
        sim = sim*(0.5*len(user_rank)/len(l_temp_f))
        if sim > temp_sim:
            temp_sim = sim
            final_id = file_rate.user_id[i]
        sim = 0.0
    return final_id


def user_kind(user_rank):
    # 汇总用户电影类别
    genres_u = {'unknown': 0, 'Action': 0, 'Adventure': 0, 'Animation': 0,
                "Children": 0, 'Comedy': 0, 'Crime': 0, 'Documentary': 0, 'Drama': 0,
                'Fantasy': 0, 'Film-Noir': 0, 'Horror': 0, 'Musical': 0, 'Mystery': 0,
                'Romance': 0, 'Sci-Fi': 0, 'Thriller': 0, 'War': 0, 'Western': 0, 'IMAX': 0}

    # 先求个用户的平均分
    temp_a = 0.0
    for i in user_rank:
        temp_a = temp_a + float(i.text)
    temp_a = temp_a / len(user_rank)

    # 用tittle去匹配找到对应的电影id
    film_list = Film.objects.all()
    l_u_mid = []
    for i in user_rank:
        for ii in film_list:
            if i.name == ii.title:
                l_u_mid.append(ii.movieid)

    for n, m in enumerate(l_u_mid):
        for ii in range(len(m_f) - 1):
            # print(m_f.movieId[ii+1])
            if int(m_f.movieId[ii + 1]) == int(m):
                temp_l = (m_f.genres[ii + 1]).split('|')
                if float(user_rank[n].text) > float(temp_a):
                    # 比平均分高说明又这个类别喜欢，这个电影也喜欢
                    for iii in temp_l:
                        genres_u[iii] = genres_u[iii] + 1
                else:
                    # 比平均分低说明这个类别喜欢，这个电影不怎么喜欢
                    for iii in temp_l:
                        genres_u[iii] = genres_u[iii] + 0.5
                for iii in temp_l:
                    genres_u[iii] = genres_u[iii] + 1
    sort_a = sorted(genres_u.items(), key=lambda item: item[1], reverse=True)

    if len(sort_a) >= 3:
        sort_a = sort_a[0:3]

    return (sort_a)


def item_cf(result_id, user_rank, genres_like):
    # 第一步找出相似用户中目标用户没看过的作为推荐电影的总集合
    movie_all = file_rate.movie_all[result_id-1]
    point_all = file_rate.point_all[result_id-1]
    movie_all = movie_all.strip('[]').split(',')
    point_all = point_all.strip('[]').split(',')
    movie_min = []
    movie_final = []

    # 用tittle去匹配找到对应的电影id,和类别
    film_list = Film.objects.all()
    l_u_mid = []
    for i in user_rank:
        for ii in film_list:
            if i.name == ii.title:
                l_u_mid.append(ii.movieid)

    # 找到匹配用户看过而待推荐用户没看过的
    for n, i in enumerate(movie_all):
        if int(i) not in l_u_mid and float(point_all[n]) >= float(file_rate.average[result_id-1]):
            movie_min.append((i, point_all[n]))
    if len(movie_min) >= 50:
        movie_min = sorted(movie_min, key=lambda item: item[1], reverse=True)[0:50]
    # 第一次尝试发现速度太慢，可能是差集里面的电影太多。先根据平均分去除一半,
    # 找出总集合中电影类型为user_rank中的电影。有匹配到类型且超过平均分，匹配到但没超过平均分都可进行推荐。
    # 匹配到类会有几等，最喜欢的，次喜欢的，较喜欢的，依次可得1,2,3
    # 原用户对该电影的评价也有一定影响，如果喜欢系数为1，不喜欢系数为0.8，主要还是看匹配类别

    for i in movie_min:
        for ii in range(len(m_f)-1):
            rec = 0.0
            if int(i[0]) == int(m_f.movieId[ii+1]):
                temp_genres = m_f.genres[ii+1]
                temp_genres = temp_genres.strip('[]').split('|')
                for g in temp_genres:
                    if g == genres_like[0][0]:
                        rec = rec + 3.0
                    if g == genres_like[1][0]:
                        rec = rec + 2.0
                    if g == genres_like[2][0]:
                        rec = rec + 1.0
                if int(i[0]) in pop:
                    rec = rec * random.random() * 0.8
                    # 惩罚流行电影
                movie_final.append((i[0], rec))
    sort_result = sorted(movie_final, key=lambda item: item[1], reverse=True)
    if len(movie_final) >= 6:
        return sort_result[0:6]
    else:
        # 防止比较用户的电影数量太少不符合
        return sort_result


def Filmfinder(user_input):
    film_file = pandas.read_csv("movies.csv", names=['movie_id', 'title', 'geners', 'average', 'account'], nrows=9126)
    film_col = []
    for n in range(len(film_file)):
        film_col.append(film_file.title[n])
    suggestions = []
    pattern = '.*'.join(user_input)  # Converts 'djm' to 'd.*j.*m'
    regex = re.compile(pattern)  # Compiles a regex.
    for item in film_col:
        match = regex.search(item)  # Checks if the current item matches the regex.
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    # print(suggestions)
    return [x for _, _, x in sorted(suggestions)]