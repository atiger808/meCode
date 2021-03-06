//index.js
//获取应用实例
var app = getApp()
var array = [];
var z=0;
Page({
  data: {
    nuberID : app.globalData.numberID,
    numberMoney :app.globalData.numberMoney,
    colorArray: ['red', 'green'],
    text: [],
    textto:"",
    key:'99',
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    config: {
      tipsshow1: "",
      tipsshow2: " "
    },
    list:
      {
      four: [
        "鸡", "飞", "狗", "跳"
      ],
      fourShow: [
        "鸡", "七", "飞", "水", "杯", "狗", "无", "捞", "盾", "收", "跳", "远", "有", "熊", "鸟", "空", "上", "前"
      ]},
    four: ["鸡", "飞", "狗", "跳"]

  },

  // 向输入框添加字符
  goText:function(e){//点击事件把选取字
    var page=this;
    let showTexts = e._relatedInfo.anchorRelatedText;//点击获得的值 
    let index = e.currentTarget.dataset.index;
    let fourShow_id = e.currentTarget.id; 
    var fours = page.data.list.four;
    let fourShows = page.data.list.fourShow;
    let newfourShow = fourShows.splice(fourShow_id, 1,'');
    var texts=page.data.text;
    var obj = {};
      obj.id = fourShow_id;
      obj.name = showTexts;
      array.push(obj);
      console.log(array)
    this.setData({
      text: array,
      z:z++,
      list:{
        fourShow:fourShows,
      }
    });

    if(array.length==4){
      var four=this.data.four;
      var msg_1='';
      var msg_2='';
      for(let i=0; i<four.length; i++){
        msg_1 += four[i]
      }
      for(let j=0; j<array.length; j++){
        msg_2 += array[j].name
      }
      if(msg_1 == msg_2){
        wx.redirectTo({
          url: '../Interpret/Interpret'
        })
        // 将numberID，numberMoney保存本地缓存
        var developer = {
          numberID: app.globalData.numberID += 1,
          numberMoney: app.globalData.numberMoney += 5
        }
        wx.setStorageSync('developer', developer); 
      }
      else{
        wx.showModal({
          title: '猜一猜',
          content: '亲！ 猜错了~~'
        })
        array.splice(0, array.length)
      }
    }
    // 如果输入字符大于5，跳转
    if(z==5){
      wx.redirectTo({
        url: '../index/index'
      })
    }
  },

  //从输入框减掉字符
  backText:function(e){
    var page = this;
    let index = e.currentTarget.dataset.index;
    let text_id = e.currentTarget.id;
    let showTexts = e._relatedInfo.anchorRelatedText;
    let texts = page.data.text;
    let fours = page.data.list.four;
    let newTexts=texts.splice(index,1, '');
    let fourShows = page.data.list.fourShow;
    let textodd = fourShows.splice(text_id, 1, showTexts);
    array.splice(index, 1);
    this.setData({
      text: texts,
      z: z--,
      list: {
        fourShow: fourShows,
      }
    });
  },


  onReady: function(){
    var page = this;
    var text = page.data.text.length;
    if(text == 0){
      setTimeout(function () {
        wx.showModal({
          title: '！！！',
          content: '请以次点击 > 鸡飞狗跳 > 成语',
        })
      },2000)
    } 
  },
  
  onLoad:function(){
    array.splice(0, array.length);
    z=0;
    var numberIDs = app.globalData.numberID;
    var numberMoneys = app.globalData.numberMoney;
    this.setData({
      numberID:numberIDs,
      numberMoney:numberMoneys,
      text:[],
    })
  },

  onShow:function(){
    var page = this
    console.log(z)
  },


  onShareAppMessage: function () {
    return {
      title: '我已闯过4关，敢否应站？',
      path: 'pages/index/index',
      success: function (res) {
        console.log(res)
      },
      fail: function (res) {
        console.log(res)
      }
    }
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },



  locaAlert:function(e){//   提示
  var page =this;
    wx.showModal({
      title: '提示',
      content:'当前缺少5金币！只需要0.99元就过此关，还永久去广告，是否前往看看',
      showCancel: true,
      cancelText: '取消',
      cancelColor: '#000000',
      confirmText: '去看看',
      confirmColor: '#008000',
      success: function(res) {
        if(res.cancel){
          wx.showToast({
            title: '分享可获得金币',
            duration:2000,
          })
        }else{
        wx.navigateTo({
          url: '../play/play',
        })
        }
      },
      fail: function(res) {},
      complete: function(res) {},
    })
  },


  play:function(){
    wx.requestPayment({
        'timeStamp': '',
        'nonceStr': '',
        'package': '',
        'signType': 'MD5',
        'paySign': '',
        'success': function (res) { },
        'fail': function (res) { },
        'complete': function (res) { }
      })
  }
})



/**
 * 1.答题框  4个
 * 
 * 
 * 2.备用选项 8个
 * 
 * 用户只能点击备用选项，才能进行答题，并且不能进入输入
 * 
 * 
 *  1.Text 显示文本  4个  
 *  2.buttom  显示八个   buttom-value 是备用选项名称
 * 
 * 
 * 3.用户点击备用选项
 *  1).判断答题框用户填入到第几个，
 *      填入一个变量加一。
 *      填入后判断 变量的值是不是等于4, 也就是 判断答题框是不是填完了 
 *       a.填完了，
 *          获取按顺序获取4个答题框的值，存放在一个字符串里
 *          判断字符串里面的值 和  答案 是否一样，
 *            a.一样，就恭喜过关
 * 
 *            b.不一样，提示不过关
 *                是否清空已知答案 
 * 
 *       b.没有填完
 *          不处理
 * 
 *   
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 */