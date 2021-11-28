import asyncio, discord, time, random, os
from discord.ext import commands

from openpyxl import load_workbook, Workbook

from user import *

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("이제 {0.user} 으로 온라인 상태임".format(bot))

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = "Our Sandbox Network", description = "시험 제작중인 봇입니다", color = 0x6E17E3) 
    embed.add_field(name = bot.command_prefix + "도움", value = "모든 명령어를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "회원가입", value = "데이터베이스에 가입하여 추가기능 사용 권한을 얻습니다", inline = False)
    embed.add_field(name = bot.command_prefix + "회원탈퇴", value = "모든 기록을 데이터베이스에서 제거합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "내정보", value = "나의 정보를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "정보 [대상]", value = "멘션한 [대상]의 정보를 확인합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "송금 [대상] [돈]", value = "멘션 [대상]에게 [돈]을 보냅니다", inline = False)
    embed.add_field(name = bot.command_prefix + "도박 [돈]", value = "[돈] 을 걸어 도박을 합니다\n누적 잃은 돈은 정보에서 확인이 가능합니다", inline = False)
    embed.add_field(name = bot.command_prefix + "가위바위보 [가위/바위/보]", value = "봇과 가위바위보를 합니다", inline = False)
    embed.set_footer(text="제작: joon00#4503")
    await ctx.send(embed=embed)

@bot.command()
    result, _color, bot, user = dice()

    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        embed = discord.Embed(title = "❌   데이터베이스 가입필요", description = "회원가입 후에 사용이 가능합니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title = "주사위 게임 결과", description = None, color = _color)
        embed.add_field(name = "Super Bot의 숫자", value = ":game_die: " + bot, inline = True)
        embed.add_field(name = ctx.author.name+"의 숫자", value = ":game_die: " + user, inline = True)
        embed.set_footer(text="결과: " + result)
        await ctx.send(embed=embed)

def dice():
    print("game.py - dice")
    a = random.randrange(1,7)
    b = random.randrange(1,7)

    if a > b:
        return "패배", 0xFF0000, str(a), str(b)
    elif a == b:
        return "무승부", 0xFAFA00, str(a), str(b)
    elif a < b:
        return "승리", 0x00ff56, str(a), str(b)

@bot.command()
async def 가위바위보(ctx, user: str):  # user:str로 !game 다음에 나오는 메시지를 받아줌
    rps_table = ['가위', '바위', '보']
    bot = random.choice(rps_table)
    result = rps_table.index(user) - rps_table.index(bot)  # 인덱스 비교로 결과 결정
    
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        embed = discord.Embed(title = "❌   데이터베이스 가입필요", description = "회원가입 후에 사용이 가능합니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        if result == 0:
            await ctx.send("가위바위보 결과를 기다리는 중...")
            await asyncio.sleep(1.2)
        
            embed = discord.Embed(title = "가위바위보 결과", description = "나의 운을 시험해봅니다", color = 0xFAFA00)
            embed.add_field(name = "가위바위보 봇 │", value = f"{user}", inline = True)
            embed.add_field(name = ctx.author.name+"", value = f"{bot}", inline = True)
            embed.set_footer(text="결과: 무승부")
            await ctx.send(embed=embed)
        elif result == 1 or result == -2:
            await ctx.send("가위바위보 결과를 기다리는 중...")
            await asyncio.sleep(1.2)
        
            embed = discord.Embed(title = "가위바위보 결과", description = "나의 운을 시험해봅니다", color = 0x00ff56)
            embed.add_field(name = "가위바위보 봇 │", value = f"{user}", inline = True)
            embed.add_field(name = ctx.author.name+"", value = f"{bot}", inline = True)
            embed.set_footer(text="결과: 승리")
            await ctx.send(embed=embed)
        else:
            await ctx.send("가위바위보 결과를 기다리는 중...")
            await asyncio.sleep(1.2)
        
            embed = discord.Embed(title = "가위바위보 결과", description = "나의 운을 시험해봅니다", color = 0xFF0000)
            embed.add_field(name = "가위바위보 봇 │", value = f"{user}", inline = True)
            embed.add_field(name = ctx.author.name+"", value = f"{bot}", inline = True)
            embed.set_footer(text="결과: 패배")
            await ctx.send(embed=embed)

@bot.command()
async def 도박(ctx, money):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    win = gamble()
    result = ""
    betting = 0
    _color = 0x000000
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        cur_money = getMoney(ctx.author.name, userRow)

        if money == "올인":
            betting = cur_money
            if win:
                result = "성공"
                _color = 0x00ff56
                print(result)

                modifyMoney(ctx.author.name, userRow, int(0.5*betting))

            else:
                result = "실패"
                _color = 0xFF0000
                print(result)

                modifyMoney(ctx.author.name, userRow, -int(betting))
                addLoss(ctx.author.name, userRow, int(betting))

            embed = discord.Embed(title = "도박 결과", description = result, color = _color)
            embed.add_field(name = "배팅금액", value = betting, inline = False)
            embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)

            await ctx.send(embed=embed)
            
        elif int(money) >= 10:
            if cur_money >= int(money):
                betting = int(money)
                print("배팅금액: ", betting)
                print("")

                if win:
                    result = "성공"
                    _color = 0x00ff56
                    print(result)

                    modifyMoney(ctx.author.name, userRow, int(0.5*betting))

                else:
                    result = "실패"
                    _color = 0xFF0000
                    print(result)

                    modifyMoney(ctx.author.name, userRow, -int(betting))
                    addLoss(ctx.author.name, userRow, int(betting))

                embed = discord.Embed(title = "도박 결과", description = result, color = _color)
                embed.add_field(name = "배팅금액", value = betting, inline = False)
                embed.add_field(name = "현재 자산", value = getMoney(ctx.author.name, userRow), inline = False)

                await ctx.send(embed=embed)

            else:
                print("돈이 부족합니다.")
                print("배팅금액: ", money, " | 현재자산: ", cur_money)
                await ctx.send("돈이 부족합니다. 현재자산: " + str(cur_money))
        else:
            print("배팅금액", money, "가 10보다 작습니다.")
            await ctx.send("10원 이상만 배팅 가능합니다.")
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        embed = discord.Embed(title = "❌   데이터베이스 가입필요", description = "회원가입 후에 사용이 가능합니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    print("------------------------------\n")

def gamble():
    print("game.py - coin")
    coin_face = random.randrange(0,2)
    
    if coin_face == 0:
        print("성공")
        return True
    else:
        print("실패")
        return False

@bot.command()
async def 랭킹(ctx):
    rank = ranking()
    embed = discord.Embed(title = "레벨 랭킹", description = None, color = 0x4A44FF)

    for i in range(0,len(rank)):
        if i%2 == 0:
            name = rank[i]
            lvl = rank[i+1]
            embed.add_field(name = str(int(i/2+1))+"위 "+name, value ="레벨: "+str(lvl), inline=False)

    await ctx.send(embed=embed) 

@bot.command()
async def 회원가입(ctx):
    print("회원가입이 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        print("DB에서 ", ctx.author.name, "을 찾았습니다.")
        print("------------------------------\n")
        embed = discord.Embed(title = "❌   회원가입 실패", description = "이미 데이터베이스에 가입하셨습니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("")

        Signup(ctx.author.name, ctx.author.id)

        print("회원가입이 완료되었습니다.")
        print("------------------------------\n")
        embed = discord.Embed(title = "✅   회원가입 완료", description = "성공적으로 데이터베이스에 가입되셨습니다.", color = 0x2fc38d)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

@bot.command()
async def 회원탈퇴(ctx):
    print("탈퇴가 가능한지 확인합니다.")
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)
    if userExistance:
        DeleteAccount(userRow)
        print("탈퇴가 완료되었습니다.")
        print("------------------------------\n")

        embed = discord.Embed(title = "✅   회원탈퇴 완료", description = "모든 정보가 데이터베이스에서 제거되었습니다.", color = 0x2fc38d)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")

        embed = discord.Embed(title = "❌   회원탈퇴 실패", description = "회원가입하지 않은 사람은 할수없습니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

@bot.command()
async def 내정보(ctx):
    userExistance, userRow = checkUser(ctx.author.name, ctx.author.id)

    if not userExistance:
        print("DB에서 ", ctx.author.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        embed = discord.Embed(title = "❌   데이터베이스 가입필요", description = "회원가입 후에 사용이 가능합니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        expToUP = level*level + 6*level
        boxes = int(exp/expToUP*20)
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = ctx.author.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "XP: " + str(exp) + "/" + str(expToUP), value = boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline = False)
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)
        embed.set_footer(text="데이터 베이스 손상 시 문의하시길 바랍니다 │ joon00#4503")

        await ctx.send(embed=embed)

@bot.command()
async def 정보(ctx, user: discord.User):
    userExistance, userRow = checkUser(user.name, user.id)

    if not userExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        await ctx.send(user.name  + " 은(는) 등록되지 않은 사용자입니다.")
    else:
        level, exp, money, loss = userInfo(userRow)
        rank = getRank(userRow)
        userNum = checkUserNum()
        print("------------------------------\n")
        embed = discord.Embed(title="유저 정보", description = user.name, color = 0x62D0F6)
        embed.add_field(name = "레벨", value = level)
        embed.add_field(name = "경험치", value = str(exp) + "/" + str(level*level + 6*level))
        embed.add_field(name = "순위", value = str(rank) + "/" + str(userNum))
        embed.add_field(name = "보유 자산", value = money, inline = False)
        embed.add_field(name = "도박으로 날린 돈", value = loss, inline = False)

        await ctx.send(embed=embed)

@bot.command()
async def 송금(ctx, user: discord.User, money):
    print("송금이 가능한지 확인합니다.")
    senderExistance, senderRow = checkUser(ctx.author.name, ctx.author.id)
    receiverExistance, receiverRow = checkUser(user.name, user.id)

    if not senderExistance:
        print("DB에서", ctx.author.name, "을 찾을수 없습니다")
        print("------------------------------\n")
        embed = discord.Embed(title = "❌   데이터베이스 가입필요", description = "회원가입 후에 사용이 가능합니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    elif not receiverExistance:
        print("DB에서 ", user.name, "을 찾을 수 없습니다")
        print("------------------------------\n")
        embed = discord.Embed(title = "❌   미등록된 사용자", description = "등록되지 않은 사용자입니다.", color = 0x800000)
        embed.set_footer(text = f"{ctx.message.author.name} | 제작: joon00#4503", icon_url = ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        print("송금하려는 돈: ", money)

        s_money = getMoney(ctx.author.name, senderRow)
        r_money = getMoney(user.name, receiverRow)

        if s_money >= int(money) and int(money) != 0:
            print("돈이 충분하므로 송금을 진행합니다.")
            print("")

            remit(ctx.author.name, senderRow, user.name, receiverRow, money)

            print("송금이 완료되었습니다. 결과를 전송합니다.")

            embed = discord.Embed(title="송금 완료", description = "송금된 돈: " + money, color = 0x77ff00)
            embed.add_field(name = "보낸 사람: " + ctx.author.name, value = "현재 자산: " + str(getMoney(ctx.author.name, senderRow)))
            embed.add_field(name = "→", value = ":moneybag:")
            embed.add_field(name="받은 사람: " + user.name, value="현재 자산: " + str(getMoney(user.name, receiverRow)))
                    
            await ctx.send(embed=embed)
        elif int(money) == 0:
            await ctx.send("0원을 보낼 필요는 없죠")
        else:
            print("돈이 충분하지 않습니다.")
            print("송금하려는 돈: ", money)
            print("현재 자산: ", s_money)
            await ctx.send("돈이 충분하지 않습니다. 현재 자산: " + str(s_money))

        print("------------------------------\n")

"""
@bot.command()
async def reset(ctx):
    resetData()
"""

@bot.command()
async def add(ctx, money):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addMoney(row, int(money))
    print("money")

@bot.command()
async def exp(ctx, exp):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    addExp(row, int(exp))
    print("exp")

@bot.command()
async def lvl(ctx, lvl):
    user, row = checkUser(ctx.author.name, ctx.author.id)
    adjustlvl(row, int(lvl))
    print("lvl")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "!reset":
        await bot.process_commands(message)
        return
    else:
        userExistance, userRow = checkUser(message.author.name, message.author.id)
        channel = message.channel
        if userExistance:
            levelUp, lvl = levelupCheck(userRow)
            if levelUp:
                print(message.author, "가 레벨업 했습니다")
                print("")
                embed = discord.Embed(title = "레벨업", description = None, color = 0x00A260)
                embed.set_footer(text = message.author.name + "이 " + str(lvl) + "레벨 달성!")
                await channel.send(embed=embed)
            else:
                modifyExp(userRow, 1)
                print("------------------------------\n")

        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "❓   잘못된 명령어", description = "잘못된 명령어입니다. !도움 으로 명령어를 확인하세요.", color = 0x800000)
        await ctx.send(embed=embed)
        
        
access_token = os.environ["BOT_TOKEN"]
bot.run(access_token)
