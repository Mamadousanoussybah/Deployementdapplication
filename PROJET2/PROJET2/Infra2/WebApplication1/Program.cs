using Azure.Identity;
using Microsoft.Extensions.Configuration;


var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorPages();

string KeyVaultURI = Environment.GetEnvironmentVariable("KeyVaultUri");
Console.WriteLine("KeyVault URI : " + KeyVaultURI);

builder.Configuration.AddAzureKeyVault(
    new Uri(KeyVaultURI),
    new DefaultAzureCredential());

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}

app.UseRouting();

app.UseAuthorization();

app.MapStaticAssets();
app.MapRazorPages()
   .WithStaticAssets();

app.Run();
