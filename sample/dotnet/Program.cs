using System;
using System.IO;
using Amazon;
using Amazon.S3;
using Amazon.S3.Model;

class MinioFileManager
{
    private static readonly string minioUrl = "http://localhost:9000";
    private static readonly string accessKey = "minioadmin";
    private static readonly string secretKey = "minioadmin";
    private static readonly string bucketName = "upload";

    private static readonly AmazonS3Client s3Client = new AmazonS3Client(
        accessKey, secretKey, new AmazonS3Config
        {
            ServiceURL = minioUrl,
            ForcePathStyle = true, 
            SignatureVersion = "v4"
        }
    );

    public static async Task UploadFile(string filePath, string objectName)
    {
        try
        {
            var putRequest = new PutObjectRequest
            {
                BucketName = bucketName,
                Key = objectName,
                FilePath = filePath
            };
            await s3Client.PutObjectAsync(putRequest);
            Console.WriteLine($"Arquivo '{objectName}' carregado com sucesso no bucket '{bucketName}'.");
        }
        catch (Exception e)
        {
            Console.WriteLine($"Erro ao fazer upload: {e.Message}");
        }
    }

    public static async Task DownloadFile(string objectName, string downloadPath)
    {
        try
        {
            var getRequest = new GetObjectRequest
            {
                BucketName = bucketName,
                Key = objectName
            };

            using (GetObjectResponse response = await s3Client.GetObjectAsync(getRequest))
            using (Stream responseStream = response.ResponseStream)
            using (var fileStream = File.Create(downloadPath))
            {
                responseStream.CopyTo(fileStream);
            }
            Console.WriteLine($"Arquivo '{objectName}' baixado com sucesso para '{downloadPath}'.");
        }
        catch (Exception e)
        {
            Console.WriteLine($"Erro ao fazer download: {e.Message}");
        }
    }

    public static void Main(string[] args)
    {
        string localFilePath = "/home/guilherme/source/pocs/file-upload/sample/dotnet/local_upload.txt";
        string downloadPath = "/home/guilherme/source/pocs/file-upload/sample/dotnet/local_download.txt";
        string objectName = "local_upload.txt";

        UploadFile(localFilePath, objectName).Wait();
        DownloadFile(objectName, downloadPath).Wait();
    }
}
