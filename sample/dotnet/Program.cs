using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string authUrl = "http://localhost:8080/auth/v1.0";
        string username = "test:tester";
        string password = "testing";
        string containerName = "mycontainer";

        // Autenticação no Swift
        var httpClient = new HttpClient();
        httpClient.DefaultRequestHeaders.Add("X-Auth-User", username);
        httpClient.DefaultRequestHeaders.Add("X-Auth-Key", password);
        var authResponse = await httpClient.GetAsync(authUrl);
        authResponse.EnsureSuccessStatusCode();

        // Obtenção do token e URL de armazenamento
        string authToken = authResponse.Headers.GetValues("X-Auth-Token").FirstOrDefault();
        string storageUrl = authResponse.Headers.GetValues("X-Storage-Url").FirstOrDefault();

        // Verificação do container
        var request = new HttpRequestMessage(HttpMethod.Head, $"{storageUrl}/{containerName}");
        request.Headers.Add("X-Auth-Token", authToken);
        
        var response = await httpClient.SendAsync(request);
        if (response.IsSuccessStatusCode)
        {
            Console.WriteLine($"O container '{containerName}' já existe.");
        }
        else if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            Console.WriteLine($"O container '{containerName}' não existe. Criando...");
            // Código para criar o container
        }
        else
        {
            Console.WriteLine("Erro ao verificar a existência do container.");
        }
    }
}
