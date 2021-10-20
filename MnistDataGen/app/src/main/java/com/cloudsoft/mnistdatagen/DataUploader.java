package com.cloudsoft.mnistdatagen;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.os.Build;
import android.os.StrictMode;
import android.util.Base64;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class DataUploader {
//    @TargetApi(Build.VERSION_CODES.GINGERBREAD)
//    @SuppressLint("NewApi")
    public static boolean upload(String b64, int type){
        String upload_url = "http://192.168.20.61:8080/pyocr/savetraindata";
//        String upload_url = "http://192.168.6.30:30956/pyocr/savetraindata";
        HttpURLConnection connection = null;
        try{
//            Log.i("mnist:","上传信息："+dataJson);
            URL url = new URL(upload_url);//放网站
            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            httpURLConnection.setRequestProperty("Charset", "utf-8");

            DataOutputStream dop = new DataOutputStream(
                    httpURLConnection.getOutputStream());
            dop.writeBytes("b64="+b64+"&type="+type);
            int responseCode = httpURLConnection.getResponseCode();
            Log.i("mnist", "responseCode = "+responseCode);
            DataInputStream dip = new DataInputStream(
                    httpURLConnection.getInputStream());
            dop.flush();
            dop.close();
        }catch (MalformedURLException e) {
            e.printStackTrace();
            return false;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }
        return true;
    }

    public static boolean upload2(String paths, String type){
        String upload_url = "http://192.168.20.61:8080/mnist/detectxy2";
        HttpURLConnection connection = null;
        try{
//            Log.i("mnist:","上传信息："+dataJson);
            URL url = new URL(upload_url);//放网站
            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            httpURLConnection.setRequestProperty("Charset", "utf-8");

            DataOutputStream dop = new DataOutputStream(
                    httpURLConnection.getOutputStream());
            Log.i("mnist", type);
            dop.writeBytes("paths="+paths+"&type="+Base64.encodeToString(type.getBytes(),Base64.DEFAULT));
            int responseCode = httpURLConnection.getResponseCode();
            Log.i("mnist", "responseCode = "+responseCode);
            DataInputStream dip = new DataInputStream(
                    httpURLConnection.getInputStream());
            dop.flush();
            dop.close();
        }catch (MalformedURLException e) {
            e.printStackTrace();
            return false;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }
        return true;
    }

    public static String upload3(String paths){
        String upload_url = "http://192.168.20.61:8080/mnist/detectxy";
//        upload_url = "http://192.168.6.30:32049/mnist/detectxy";
//        upload_url = "http://192.168.6.35:31291/mnist/detectxy";
        HttpURLConnection connection = null;
        try{
//            Log.i("mnist:","上传信息："+dataJson);
            URL url = new URL(upload_url);//放网站
            HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
            httpURLConnection.setDoInput(true);
            httpURLConnection.setDoOutput(true);
            httpURLConnection.setRequestMethod("POST");
            httpURLConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            httpURLConnection.setRequestProperty("Charset", "utf-8");

            DataOutputStream dop = new DataOutputStream(
                    httpURLConnection.getOutputStream());
            dop.writeBytes("paths="+paths);
            int responseCode = httpURLConnection.getResponseCode();

            Log.i("mnist", "responseCode = "+responseCode);
            DataInputStream dip = new DataInputStream(
                    httpURLConnection.getInputStream());
            String msg = "";
            InputStreamReader inputStreamReader = new InputStreamReader(dip);
            BufferedReader reader = new BufferedReader(inputStreamReader);// 读字符串用的。
            String tmpL;
            while((tmpL = reader.readLine())!=null){
                Log.i("mnist", tmpL);
                msg+=tmpL;
            }
            JSONObject jobj = new JSONObject(msg);
            dop.flush();
            dop.close();
            return jobj.getString("msg");
        }catch (MalformedURLException e) {
            e.printStackTrace();
            return "";
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }catch (Exception e){
            e.printStackTrace();
            return "";
        }
    }
}



